from sys import argv

from koozie import fr_u
from resdx import (
    FanMotorType,
    RESNETDXModel,
    StagingType,
    get_heating_performance_map_object,
    get_cooling_performance_map_object,
)


def get_performance_map(
    stage_type: str,
    cooling_capacity_95_btuh: str,
    heating_capacity_47_btuh: str,
    heating_capacity_17_btuh: str,
    minimum_rated_temperature_degF: str,
    seer2: str,
    eer2: str,
    hspf2: str,
    motor_type: str,
    duct_type: str,
) -> str:
    """
    Get CSE objects rsPerfMapClg and rsPerfMapHtg
    """
    stage_type = StagingType[stage_type]

    cooling_capacity_95 = fr_u(float(cooling_capacity_95_btuh), "Btu/h")
    heating_capacity_47 = fr_u(float(heating_capacity_47_btuh), "Btu/h")
    heating_capacity_17 = fr_u(float(heating_capacity_17_btuh), "Btu/h")

    minimum_rated_temperature = fr_u(float(minimum_rated_temperature_degF), "degF")

    seer2: float = float(seer2)  # type: ignore
    eer2: float = float(eer2)  # type: ignore
    hspf2: float = float(hspf2)  # type: ignore

    motor_type = FanMotorType[motor_type]

    if duct_type == "DUCTED":
        is_ducted = True
    else:  # duct_type == "DUCTLESS"
        is_ducted = False

    unit = RESNETDXModel(
        staging_type=stage_type,
        rated_net_total_cooling_capacity=cooling_capacity_95,
        rated_net_heating_capacity=heating_capacity_47,
        rated_net_heating_capacity_17=heating_capacity_17,
        heating_off_temperature=minimum_rated_temperature,
        input_seer=seer2,
        input_eer=eer2,
        input_hspf=hspf2,
        motor_type=motor_type,
        is_ducted=is_ducted,
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
    minimum_rated_temperature_degF = argv[5]
    seer2 = argv[6]
    eer2 = argv[7]
    hspf2 = argv[8]
    motor_type = argv[9]
    duct_type = argv[10]

    print(
        get_performance_map(
            stage_type=stage_type,
            cooling_capacity_95_btuh=cooling_capacity_95_btuh,
            heating_capacity_47_btuh=heating_capacity_47_btuh,
            heating_capacity_17_btuh=heating_capacity_17_btuh,
            minimum_rated_temperature_degF=minimum_rated_temperature_degF,
            seer2=seer2,
            eer2=eer2,
            hspf2=hspf2,
            motor_type=motor_type,
            duct_type=duct_type,
        )
    )
