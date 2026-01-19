from sys import argv

from koozie import fr_u
from resdx import RESNETDXModel, StagingType, get_heating_performance_map_object, get_cooling_performance_map_object


def _calculate_eer_from_seer(seer: float) -> float:
    return 10.0 + 0.84 * (seer - 11.5) if seer < 13.0 else 11.3 + 0.57 * (seer - 13.0)


def _calculate_heating_capacity_17_rated(capacity_47_rated: float, stage_type: StagingType) -> float:
    if stage_type == StagingType.VARIABLE_SPEED:
        return 0.689 * capacity_47_rated
    else:  # Single or Two Speed
        return 0.626 * capacity_47_rated


def get_performance_map(
    stage_type: str,
    cooling_capacity_95_btuh: str,
    heating_capacity_47_btuh: str,
    heating_capacity_17_btuh: str,
    seer2: str,
    eer2: str,
    hspf2: str,
) -> str:
    """
    Get CSE objects rsPerfMapClg and rsPerfMapHtg
    """
    stage_type = StagingType[stage_type]

    cooling_capacity_95 = fr_u(float(cooling_capacity_95_btuh), "kBtu/h")
    heating_capacity_47 = fr_u(float(heating_capacity_47_btuh), "kBtu/h")
    heating_capacity_17 = fr_u(float(heating_capacity_17_btuh), "kBtu/h")

    seer2: float = float(seer2)  # type: ignore
    eer2: float = float(eer2)  # type: ignore
    hspf2: float = float(hspf2)  # type: ignore

    unit = RESNETDXModel(
        staging_type=stage_type,
        rated_net_total_cooling_capacity=cooling_capacity_95,
        rated_net_heating_capacity=heating_capacity_47,
        rated_net_heating_capacity_17=heating_capacity_17,
        input_seer=seer2,
        input_eer=eer2,
        input_hspf=hspf2,
    )

    system_name = "RSYS"

    heating_performance_map_object = get_heating_performance_map_object(unit=unit, system_name=system_name)
    cooling_performance_map_object = get_cooling_performance_map_object(unit=unit, system_name=system_name)

    performance_map_objects = [heating_performance_map_object, cooling_performance_map_object]

    return "\n\n".join([str(performance_map_object) for performance_map_object in performance_map_objects])


if __name__ == "__main__":
    stage_type = argv[1]
    cooling_capacity_95_btuh = argv[2]
    heating_capacity_47_btuh = argv[3]
    heating_capacity_17_btuh = argv[4]
    seer2 = argv[5]
    eer2 = argv[6]
    hspf2 = argv[7]

    print(
        get_performance_map(
            stage_type=stage_type,
            cooling_capacity_95_btuh=cooling_capacity_95_btuh,
            heating_capacity_47_btuh=heating_capacity_47_btuh,
            heating_capacity_17_btuh=heating_capacity_17_btuh,
            seer2=seer2,
            eer2=eer2,
            hspf2=hspf2,
        )
    )
