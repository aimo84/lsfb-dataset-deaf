import pytest

import os
import tempfile
import numpy as np
import pandas as pd


@pytest.fixture(scope="session")
def mock_lsfb_isol_path_v2() -> str:
    """
    Mock a lsfb isol dataset containing 10 signs label with 30 examples each.
    """

    with tempfile.TemporaryDirectory() as tmp_dirname:
        create_dummy_instances_csv(tmp_dirname)
        yield tmp_dirname


def create_dummy_instances_csv(
    root_dir: str, nbr_labels: int = 10, nbr_examples: int = 30
) -> pd.DataFrame:
    csv_path = f"{root_dir}/instances.csv"

    data = {
        "id": [],
        "sign": [],
        "signer": [],
        "start": [],
        "end": [],
    }

    for label_nbr in range(nbr_labels):
        for example in range(nbr_examples):
            start = 2500
            end = 2600

            sign = f"label{label_nbr}"
            clip_id = (
                f"CLSFBI{label_nbr:02d}{example:02d}_S0{example:02d}_B_{start}_{end}"
            )
            signer = f"S0{example}"

            data["id"].append(clip_id)
            data["sign"].append(sign)
            data["signer"].append(signer)
            data["start"].append(start)
            data["end"].append(end)

            for pose_file in ["poses", "poses_raw"]:
                create_pose_files(root_dir, clip_id, pose_file)

    df = pd.DataFrame.from_dict(data)
    df.to_csv(csv_path)

    return df


def create_pose_files(
    root_dir: str, clip_id: str, pose_folder: str, nb_frame: int = 25
) -> None:
    pose_path = f"{root_dir}/{pose_folder}"

    if os.path.exists(pose_path) == False:
        os.mkdir(pose_path)

    sub_folders = [
        {"name": "pose", "shape": (nb_frame, 33, 3)},
        {"name": "right_hand", "shape": (nb_frame, 21, 3)},
        {"name": "left_hand", "shape": (nb_frame, 21, 3)},
        {"name": "face", "shape": (nb_frame, 478, 3)},
    ]

    for sub_folder in sub_folders:
        sub_folder_path = f"{pose_path}/{sub_folder['name']}"

        if os.path.exists(sub_folder_path) == False:
            os.mkdir(sub_folder_path)

        mocked_landmarks = np.random.rand(*sub_folder["shape"])
        landmark_file = f"{sub_folder_path}/{clip_id}.npy"

        np.save(landmark_file, mocked_landmarks)
