"""Unit tests for the lightweight web application server."""
from __future__ import annotations

import pytest

from galton_webapp import server


def test_build_simulation_payload_generates_expected_shape():
    payload = {
        "num_balls": 100,
        "num_levels": 4,
        "p_right": 0.5,
        "seed": 123,
    }

    response = server.build_simulation_payload(payload)

    assert response["success"] is True
    data = response["data"]
    assert len(data["counts"]) == payload["num_levels"] + 1
    assert abs(data["mean"] - 2.0) < 1.0
    assert "ascii" in data and data["ascii"].strip() != ""
    assert data["parameters"]["seed"] == 123


def test_build_simulation_payload_applies_defaults():
    response = server.build_simulation_payload({})

    data = response["data"]
    params = data["parameters"]
    assert params["num_balls"] == server.DEFAULT_NUM_BALLS
    assert params["num_levels"] == server.DEFAULT_NUM_LEVELS
    assert abs(params["p_right"] - server.DEFAULT_P_RIGHT) < 1e-9
    assert params["seed"] is None


@pytest.mark.parametrize("seed", ["abc", 3.14, object()])
def test_build_simulation_payload_invalid_seed(seed):
    with pytest.raises(ValueError):
        server.build_simulation_payload({"seed": seed})


@pytest.mark.parametrize(
    "key,value,error_fragment",
    [
        ("num_balls", "abc", "num_balls"),
        ("num_levels", 2.7, "num_levels"),
        ("p_right", "not-a-float", "p_right"),
    ],
)
def test_build_simulation_payload_invalid_types(key, value, error_fragment):
    with pytest.raises(ValueError) as exc:
        server.build_simulation_payload({key: value})

    assert error_fragment in str(exc.value)
