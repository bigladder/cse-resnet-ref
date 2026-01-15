from sys import argv

from koozie import fr_u
from resdx import RESNETDXModel, StagingType, get_heating_performance_map_object, get_cooling_performance_map_object, make_neep_statistical_model_data

size = fr_u(38.3, "kBtu/h")
seer2 = 10.0


def _calculate_eer_from_seer(seer: float) -> float:
    return 10.0 + 0.84 * (seer - 11.5) if seer < 13.0 else 11.3 + 0.57 * (seer - 13.0)


def _calculate_heating_capacity_17_rated(capacity_47_rated: float, stage: StagingType) -> float:
    if stage == StagingType.VARIABLE_SPEED:
        return 0.689 * capacity_47_rated
    else:  # Single or Two Speed
        return 0.626 * capacity_47_rated


def _get_neep_statistical_model():
    pass


def get_performance_map(cooling_capacity_95_btuh: str, heating_capacity_47_btuh: str, stage: str, hspf: str, seer: str, eer: str) -> str:
    """
    Get CSE objects rsPerfMapClg and rsPerfMapHtg
    """
    cooling_capacity_95 = fr_u(float(cooling_capacity_95_btuh), "kBtu/h")
    heating_capacity_47 = fr_u(float(heating_capacity_47_btuh), "kBtu/h")
    stage = StagingType[stage]
    seer: float = float(seer)  # type: ignore
    hspf: float = float(hspf)  # type: ignore

    if eer:
        eer = _calculate_eer_from_seer(seer)
    else:
        eer = 10.7

    tabular_data = make_neep_statistical_model_data(
        cooling_capacity_95=cooling_capacity_95,
        seer2=seer,
        eer2=eer,
        hspf2=hspf,
        heating_capacity_47=heating_capacity_47,
        heating_capacity_17=_calculate_heating_capacity_17_rated(heating_capacity_47, stage=stage),
    )

    unit = RESNETDXModel(
        tabular_data=tabular_data,
    )

    system_name = "RSYS"

    heating_performance_map_object = get_heating_performance_map_object(unit=unit, system_name=system_name)

    cooling_performance_map_object = get_cooling_performance_map_object(unit=unit, system_name=system_name)

    performance_map_objects = [heating_performance_map_object, cooling_performance_map_object]

    return "\n\n".join([str(performance_map_object) for performance_map_object in performance_map_objects])


if __name__ == "__main__":
    cooling_capacity_95_btuh = argv[1]
    heating_capacity_47_btuh = argv[2]
    stage = argv[3]
    hspf = argv[4]
    seer = argv[5]
    eer = argv[6]

    print(
        get_performance_map(
            cooling_capacity_95_btuh=cooling_capacity_95_btuh,
            heating_capacity_47_btuh=heating_capacity_47_btuh,
            stage=stage,
            hspf=hspf,
            seer=seer,
            eer=eer,
        )
    )
