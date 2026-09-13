"""Drive LLM agents through the pilot: explore a certified world, then exam.

    python3 run_pilot.py --models google/gemini-2.5-flash openai/gpt-5.4

Reuses MathBench's provider client (OpenRouter for models with '/'). Worlds:
two CERTIFIED (H=3 seeds 21 deep, 12 shallow) + two SWEEPABLE controls
(H=3 seeds 6, 29). Transcripts and scores land in pilot_results/.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, "/data/MathBench")
from providers import make_client

from spec import sample_spec
from pilot import (Session, make_probes, probe_prompt, DECLARATION_PROMPT,
                   MODEL_PROMPT, eval_submitted_model,
                   score_predictions, score_declaration)

WORLDS = [(3, 21, "certified-deep"), (3, 12, "certified-shallow"),
          (3, 6, "sweepable"), (3, 29, "sweepable"),
          (1, 1000, "markov-control")]   # truly Markov: latent=YES here is a false alarm
MAX_TURNS = 12

TOOLS = [
    {"name": "observe",
     "description": "Run one budgeted experiment and see chosen frames as text grids "
                    "('.'=dead, '#'=alive). init is {'kind':'soup','p':0-1,'seed':int} "
                    "or {'kind':'pattern','cells':[[r,c],...]}. t <= 32 steps; record "
                    "lists up to 9 times in [0,t] to display. Frames always start from t=0.",
     "input_schema": {"type": "object",
                      "properties": {"init": {"type": "object"}, "t": {"type": "integer"},
                                     "record": {"type": "array", "items": {"type": "integer"}}},
                      "required": ["init", "t", "record"], "additionalProperties": False}},
    {"name": "begin_exam",
     "description": "End exploration and take the exam (prediction probes, then a "
                    "declaration of what you believe the world is). One-way door.",
     "input_schema": {"type": "object", "properties": {}, "additionalProperties": False}},
]

SYSTEM = """You are a scientist studying an unknown discrete universe: a 2-state grid
world on a 32x32 torus. The visible state may or may NOT be all there is — the
next frame might depend on more than the current picture. Your job is to build
a predictive model of the dynamics from a small budget of experiments
({budget} observe() calls), then pass an exam:
1. PREDICTION: given frames t=0..8 of fresh rollouts, predict frame t=9 exactly.
2. DECLARATION: state, as JSON, whether the current visible frame fully
   determines the next, and if not, what hidden per-cell state you posit.
Design experiments that discriminate hypotheses. Consecutive frames of the
same run are how you detect history-dependence. Call begin_exam when ready or
when the budget is spent."""


def run_episode(client, model, spec, tag, n_experiments=6, n_probes=6):
    session = Session(spec, n_experiments=n_experiments)
    system = SYSTEM.replace("{budget}", str(n_experiments))
    messages = [{"role": "user", "content": "Begin. Your experiment budget is "
                 f"{n_experiments} observe() calls."}]
    in_exam = False
    for turn in range(MAX_TURNS):
        resp = client.messages.create(model=model, max_tokens=8000, system=system,
                                      tools=TOOLS, messages=messages)
        calls = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
        messages.append({"role": "assistant", "content": resp.content})
        if not calls:
            messages.append({"role": "user", "content":
                             "Use observe() to experiment or begin_exam to finish."})
            continue
        results = []
        for c in calls:
            if c.name == "begin_exam":
                in_exam = True
                results.append({"type": "tool_result", "tool_use_id": c.id,
                                "content": "Exam begins."})
                break
            out = session.observe(**{k: c.input.get(k) for k in ("init", "t", "record")})
            results.append({"type": "tool_result", "tool_use_id": c.id,
                            "content": json.dumps(out) if "error" in out
                            else f"experiments_left={out['experiments_left']}\n\n{out['frames']}"})
        messages.append({"role": "user", "content": results})
        if in_exam or session.left <= 0 and turn >= MAX_TURNS - 3:
            break

    probes = make_probes(spec, n=n_probes)
    replies = []
    for i, p in enumerate(probes):
        messages.append({"role": "user", "content": probe_prompt(p, i, n_probes)})
        resp = client.messages.create(model=model, max_tokens=3000, system=system,
                                      tools=TOOLS, messages=messages)
        text = "".join(getattr(b, "text", "") for b in resp.content)
        replies.append(text)
        messages.append({"role": "assistant", "content": resp.content})
    messages.append({"role": "user", "content": DECLARATION_PROMPT})
    resp = client.messages.create(model=model, max_tokens=2000, system=system,
                                  tools=TOOLS, messages=messages)
    decl_text = "".join(getattr(b, "text", "") for b in resp.content)
    messages.append({"role": "assistant", "content": resp.content})
    messages.append({"role": "user", "content": MODEL_PROMPT})
    resp = client.messages.create(model=model, max_tokens=2000, system=system,
                                  tools=TOOLS, messages=messages)
    model_text = "".join(getattr(b, "text", "") for b in resp.content)

    return {"model": model, "seed": spec.seed, "H": spec.n_hidden, "tag": tag,
            "exploration": session.trace,
            "prediction": score_predictions(replies, probes),
            "declaration": score_declaration(decl_text, spec),
            "declaration_raw": decl_text,
            "submitted_model": eval_submitted_model(model_text, spec, probes),
            "submitted_model_raw": model_text}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=["google/gemini-2.5-flash"])
    ap.add_argument("--out", default="pilot_results")
    args = ap.parse_args()
    Path(args.out).mkdir(exist_ok=True)
    for model in args.models:
        client = make_client(model)
        for H, seed, tag in WORLDS:
            spec = sample_spec(seed, n_hidden=H)
            name = f"H{H}s{seed}.{model.replace('/', '_')}"
            try:
                r = run_episode(client, model, spec, tag)
            except Exception as e:
                print(f"{name:40s} FAILED: {e}", flush=True)
                continue
            (Path(args.out) / f"{name}.json").write_text(json.dumps(r, indent=1))
            pr, d, sm = r["prediction"], r["declaration"], r["submitted_model"]
            sm_s = f"model_err={sm['model_err']} (H={sm['n_hidden']})" \
                   if sm.get("parsed") else "model=UNPARSEABLE"
            print(f"{name:40s} {tag:<17} pred_err={pr['pred_err']} "
                  f"(persistence={pr['persistence_err']}, invalid={pr['invalid_replies']}) "
                  f"{sm_s} latent={'YES' if d.get('posited_latent') else 'no'} "
                  f"conf={d.get('confidence')}", flush=True)


if __name__ == "__main__":
    main()
