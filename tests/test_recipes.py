# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Ioannis Valasakis <tungolcild@gmail.com>
"""Recipe interpreter provenance and determinism."""

from __future__ import annotations

from artefaux.corpus import build_corpus_specs
from artefaux.recipes import build_record
from tests.conftest import make_einthoven_ecg

MASTER_SEED = 20260713


def _first_nstdb_step(label):
    return next(s for s in label.corruption_truth.steps if s.op == "nstdb_mix")


def test_nstdb_mix_records_noise_segment_offset():
    """The exact source segment must be in the audit trail, not just reproducible."""
    parent = make_einthoven_ecg(seed=3)
    spec = next(s for s in build_corpus_specs() if s.group == "real_noise")
    _, label = build_record(parent, spec, MASTER_SEED, fs=500)
    step = _first_nstdb_step(label)
    assert step.noise_source_record is not None
    assert step.noise_source_start_sample is not None
    assert step.noise_source_start_sample >= 0


def test_nstdb_mix_offset_is_deterministic():
    parent = make_einthoven_ecg(seed=3)
    spec = next(s for s in build_corpus_specs() if s.group == "real_noise")
    _, a = build_record(parent, spec, MASTER_SEED, fs=500)
    _, b = build_record(parent, spec, MASTER_SEED, fs=500)
    assert (
        _first_nstdb_step(a).noise_source_start_sample
        == _first_nstdb_step(b).noise_source_start_sample
    )
