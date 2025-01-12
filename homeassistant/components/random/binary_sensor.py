"""Support for showing random states."""
from __future__ import annotations

from collections.abc import Mapping
from random import getrandbits
from typing import Any

import voluptuous as vol

from homeassistant.components.binary_sensor import (
    DEVICE_CLASSES_SCHEMA,
    PLATFORM_SCHEMA,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_DEVICE_CLASS, CONF_NAME
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

DEFAULT_NAME = "Random Binary Sensor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_DEVICE_CLASS): DEVICE_CLASSES_SCHEMA,
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Random binary sensor."""

    async_add_entities([RandomBinarySensor(config)], True)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize config entry."""
    async_add_entities(
        [RandomBinarySensor(config_entry.options, config_entry.entry_id)], True
    )


class RandomBinarySensor(BinarySensorEntity):
    """Representation of a Random binary sensor."""

    _state: bool | None = None

    def __init__(self, config: Mapping[str, Any], entry_id: str | None = None) -> None:
        """Initialize the Random binary sensor."""
        self._name = config.get(CONF_NAME)
        self._device_class = config.get(CONF_DEVICE_CLASS)
        if entry_id:
            self._attr_unique_id = entry_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return true if sensor is on."""
        return self._state

    @property
    def device_class(self):
        """Return the sensor class of the sensor."""
        return self._device_class

    async def async_update(self) -> None:
        """Get new state and update the sensor's state."""

        self._state = bool(getrandbits(1))
