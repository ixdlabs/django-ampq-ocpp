from ocpp.utils.model.model_enum import ModelEnum


class StopReason(ModelEnum):
    EmergencyStop = "EmergencyStop"
    EVDisconnected = "EVDisconnected"
    HardReset = "HardReset"
    Local = "Local"
    Other = "Other"
    PowerLoss = "PowerLoss"
    Reboot = "Reboot"
    Remote = "Remote"
    SoftReset = "SoftReset"
    UnlockCommand = "UnlockCommand"
    DeAuthorized = "DeAuthorized"
