"""Sonoff TRVZB - Zigbee Thermostatic Radiator Valve."""

import zigpy.types as t
from zigpy.zcl.foundation import BaseAttributeDefs, DataTypeId, ZCLAttributeDef

from zhaquirks.builder import (
    NumberDeviceClass,
    QuirkBuilder,
    UnitOfTemperature,
    UnitOfTime,
)
from zhaquirks.clusters import CustomCluster

"""OnOff Cluster attribute ids."""

# OnOff, Attribute ID 0x0000, enum8
# 0x00=Off
# 0x01=On   TRVZB is in working mode

"""PowerConfiguration Cluster attribute ids."""

# Battery Percentage Remaining, Attribute ID 0x0021, uint8
# in 1/2 percent 0xC8=200=100%

"""Thermostat Cluster attribute ids."""

# LocalTemperature, Attribute ID 0x0000, int16
# temperature in 1/100th degree celsius (2140=21.40°C)

# OccupiedHeatingSetPoint, Attribute ID 0x0012, int16
# temperature in 1/100th degree celsius (3500=35.00°C)

# SystemMode, Attribute ID 0x001c, enum8
# 0x00=Anti Freeze (reports back OccupiedHeatingSetPoint 0x0012 and LocalTemperature 0x0000)
# 0x01=Auto (scheduler activated)
# 0x04=Manual or Boost or Scheduled Override Active

# LocalTempreatureCalibration, Attribute ID 0x0010, int8
# in 1/10th degree celsius (-2=-0.2°C)

# Thermostat Running State, Attribute ID 0x0029, bitmap16
# 0x01=Heating

"""SONOFF CustomCluster specific thermostat attribute ids."""

# Adaptive Mode, Attribute ID 0x6013, enum8
# 0x00=Inactive (Valve opening percentage and temperature accuracy possible)
# 0x02=Active (Valve opening based on target temperature and temperature changes)

# Child Lock, Attribute ID 0x0000, Bool
# 0x00=False (TRV can be operated)
# 0x01=True (TRV operation blocked)

# Open Window Detection, Attribute 0x6000, Bool
# 0x00=False
# 0x01=True (temperature drop of >1.5°C in 4.5 minutes, target temperature 12°C)

# Temporary Activation Mode, Attribute ID 0x6014, uint8
# 0x00=Boost (set 0x6015 activation time first)
# 0x01=Scheduled (set 0x6015 activation time and 0x6016 temperature first)

# Temporary Activation Time, Attibute ID 0x6015, uint32
# activation time in seconds (900=15 minutes)

# Temporary Target Temperature, Attribute ID 0x6016, int16
# 500=5.0°C temperature in 1/100th degree celsius

# ???, Attribute ID 0x6007, int16
# 1336=???  reported after starting Boost mode
# 1149=???  reported after starting boost
# 1334=???  reported after stopping boost

# ???, Attribute ID 0x6009, int16
# 1500=???  reported after starting Boost mode

# ???, Attribute ID 0x6008, uint8
# 0x7f=127=???  reported after saving scheduler

# Anti Freeze Temperature, Attribute ID 0x6002, int16
# 700=7.0°C temperature in 1/100th degree celsius

# Valve Opening Percentage, Attribute ID 0x600b, uint8
# in percent 0x64=100=100%

# Valve Closing Percentage, Attribute ID 0x600c, uint8
# in percent 0x64=100=100%

# Temperature Accuracy Adjust, Attribute ID 0x
# not, if Adaptive Mode is activated
# =-1.0°C
# =-0.8°C
# =-0.6°C
# =-0.4°C
# =-0.2°C
# doesn't want to write with firmware 1.4.4

# Display Orientation, Screen Rotation, Attribute ID 0x0021, uint8
# 0x00=Horizontal (default)
# 0x02=Vertikal (flipped)
DISPLAY_ORIENTATION_ATTR_ID = 0x0021


class DisplayOrientation(t.enum8):
    """Rotation of display orientation."""

    Rotate_0 = 0x00     # default orientation
    #Rotate_90 = 0x01
    Rotate_180 = 0x02   # flipped orientation
    #Rotate_270 = 0x03


class CustomSonoffCluster(CustomCluster):
    """Custom Sonoff cluster."""

    cluster_id = 0xFC11

    class AttributeDefs(BaseAttributeDefs):
        """Attribute definitions."""

        child_lock = ZCLAttributeDef(
            id=0x0000,
            type=t.Bool,
            manufacturer_code=None,
        )
        open_window = ZCLAttributeDef(
            id=0x6000,
            type=t.Bool,
            manufacturer_code=None,
        )
        frost_protection_temperature = ZCLAttributeDef(
            id=0x6002,
            type=t.int16s,
            manufacturer_code=None,
        )
        idle_steps = ZCLAttributeDef(
            id=0x6003,
            type=t.uint16_t,
            access="r",
            manufacturer_code=None,
        )
        closing_steps = ZCLAttributeDef(
            id=0x6004,
            type=t.uint16_t,
            access="r",
            manufacturer_code=None,
        )
        valve_opening_limit_voltage = ZCLAttributeDef(
            id=0x6005,
            type=t.uint16_t,
            access="r",
            manufacturer_code=None,
        )
        valve_closing_limit_voltage = ZCLAttributeDef(
            id=0x6006,
            type=t.uint16_t,
            access="r",
            manufacturer_code=None,
        )
        valve_motor_running_voltage = ZCLAttributeDef(
            id=0x6007,
            type=t.uint16_t,
            access="r",
            manufacturer_code=None,
        )
        valve_opening_degree = ZCLAttributeDef(
            id=0x600B,
            type=t.uint8_t,
            manufacturer_code=None,
        )
        valve_closing_degree = ZCLAttributeDef(
            id=0x600C,
            type=t.uint8_t,
            manufacturer_code=None,
        )
        external_temperature_sensor_enable = ZCLAttributeDef(
            id=0x600E,
            type=t.uint8_t,
            manufacturer_code=None,
        )
        external_temperature_sensor_value = ZCLAttributeDef(
            id=0x600D,
            type=t.int16s,
            manufacturer_code=None,
        )
        temperature_control_accuracy = ZCLAttributeDef(
            id=0x6011,
            type=t.int16s,
            manufacturer_code=None,
        )
        temporary_mode = ZCLAttributeDef(
            id=0x6014,
            type=t.uint8_t,
            manufacturer_code=None,
        )
        temporary_mode_duration = ZCLAttributeDef(
            id=0x6015,
            type=t.uint32_t,
            manufacturer_code=None,
        )
        timer_mode_target_temperature = ZCLAttributeDef(
            id=0x6016,
            type=t.int16s,
            manufacturer_code=None,
        )
        smart_temperature_control = ZCLAttributeDef(
            id=0x6017,
            type=t.bitmap8,
            manufacturer_code=None,
        )
        display_orientation = ZCLAttributeDef(
            id=DISPLAY_ORIENTATION_ATTR_ID,
            type=DisplayOrientation,
            zcl_type=DataTypeId.uint8,
            manufacturer_code=None,
        )


(
    QuirkBuilder("SONOFF", "TRVZB")
    .replaces(CustomSonoffCluster)
    .switch(
        CustomSonoffCluster.AttributeDefs.smart_temperature_control.name,
        # ControlModeType,
        CustomSonoffCluster.cluster_id,
        on_value=2,
        off_value=0,
        translation_key="adaptive_mode",
        fallback_name="Adaptive mode",
    )
    .switch(
        CustomSonoffCluster.AttributeDefs.child_lock.name,
        CustomSonoffCluster.cluster_id,
        translation_key="child_lock",
        fallback_name="Child lock",
    )
    .switch(
        CustomSonoffCluster.AttributeDefs.open_window.name,
        CustomSonoffCluster.cluster_id,
        translation_key="open_window",
        fallback_name="Open window",
    )
    .number(
        CustomSonoffCluster.AttributeDefs.timer_mode_target_temperature.name,
        CustomSonoffCluster.cluster_id,
        min_value=4.0,
        max_value=35.0,
        step=0.5,
        device_class=NumberDeviceClass.TEMPERATURE,
        unit=UnitOfTemperature.CELSIUS,
        multiplier=0.01,
        translation_key="timer_mode_target_temperature",
        fallback_name="Timer mode target temperature",
    )
    .number(
        CustomSonoffCluster.AttributeDefs.temporary_mode_duration.name,
        CustomSonoffCluster.cluster_id,
        min_value=0,
        max_value=1440,
        step=1,
        device_class=NumberDeviceClass.DURATION,
        unit=UnitOfTime.MINUTES,
        multiplier=1 / 60,
        translation_key="temporary_mode_duration",
        fallback_name="Temporary mode duration",
    )
    .write_attr_button(
        attribute_name=CustomSonoffCluster.AttributeDefs.temporary_mode.name,
        cluster_id=CustomSonoffCluster.cluster_id,
        attribute_value=0x00,
        unique_id_suffix="boost_mode",
        translation_key="boost_mode",
        fallback_name="Boost mode",
    )
    .write_attr_button(
        attribute_name=CustomSonoffCluster.AttributeDefs.temporary_mode.name,
        cluster_id=CustomSonoffCluster.cluster_id,
        attribute_value=0x01,
        unique_id_suffix="timer_mode",
        translation_key="timer_mode",
        fallback_name="Timer mode",
    )
    .number(
        CustomSonoffCluster.AttributeDefs.frost_protection_temperature.name,
        CustomSonoffCluster.cluster_id,
        min_value=4.0,
        max_value=35.0,
        step=0.5,
        device_class=NumberDeviceClass.TEMPERATURE,
        unit=UnitOfTemperature.CELSIUS,
        multiplier=0.01,
        translation_key="frost_protection_temperature",
        fallback_name="Frost protection temperature",
    )
    .number(
        CustomSonoffCluster.AttributeDefs.valve_opening_degree.name,
        CustomSonoffCluster.cluster_id,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        translation_key="valve_opening_degree",
        fallback_name="Valve opening degree",
        initially_disabled=True,
    )
    .number(
        CustomSonoffCluster.AttributeDefs.valve_closing_degree.name,
        CustomSonoffCluster.cluster_id,
        min_value=0.0,
        max_value=100.0,
        step=1.0,
        translation_key="valve_closing_degree",
        fallback_name="Valve closing degree",
        initially_disabled=True,
    )
    .number(
        CustomSonoffCluster.AttributeDefs.temperature_control_accuracy.name,
        CustomSonoffCluster.cluster_id,
        min_value=-1.0,
        max_value=-0.2,
        step=0.2,
        device_class=NumberDeviceClass.TEMPERATURE_DELTA,
        unit=UnitOfTemperature.CELSIUS,
        multiplier=0.01,
        translation_key="temperature_control_accuracy",
        fallback_name="Temperature control accuracy",
    )
    .switch(
        CustomSonoffCluster.AttributeDefs.external_temperature_sensor_enable.name,
        CustomSonoffCluster.cluster_id,
        translation_key="external_temperature_sensor",
        fallback_name="External temperature sensor",
    )
    .number(
        CustomSonoffCluster.AttributeDefs.external_temperature_sensor_value.name,
        CustomSonoffCluster.cluster_id,
        min_value=0.0,
        max_value=99.9,
        step=0.1,
        device_class=NumberDeviceClass.TEMPERATURE,
        unit=UnitOfTemperature.CELSIUS,
        multiplier=0.01,
        translation_key="external_temperature_sensor_value",
        fallback_name="External temperature sensor value",
    )
    .enum(
        attribute_name=CustomSonoffCluster.AttributeDefs.display_orientation.name,
        enum_class=DisplayOrientation,
        cluster_id=CustomSonoffCluster.cluster_id,
        translation_key="display_orientation",
        fallback_name="Display Orientation",
    )
    .add_to_registry()
)
