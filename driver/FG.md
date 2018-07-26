bq27421

instantaneous current //瞬时电流

NORMAL Mode
The fuel gauge is in NORMAL mode when not in any other power mode. During this mode,
AverageCurrent(), Voltage(), and Temperature() measurements are taken once per second, and the
interface data set is updated.


2.4.5 SLEEP Mode
SLEEP mode is entered automatically if the feature is enabled (OpConfig [SLEEP] = 1) and
AverageCurrent() is below the programmable level Sleep Current (default = 10 mA).

2.4.6 HIBERNATE Mode

Before the fuel gauge can enter HIBERNATE mode, the system must use the SET_HIBERNATE
subcommand to set the [HIBERNATE] bit of the CONTROL_STATUS register. The fuel gauge waits to
enter HIBERNATE mode until it has taken a valid OCV measurement and the magnitude of the average
cell current has fallen below Hibernate Current. The fuel gauge can also enter HIBERNATE mode if the
cell voltage falls below the Hibernate Voltage.

It is the responsibility of the system to wake the fuel gauge after it has gone into HIBERNATE mode and
to prevent a charger from charging the battery before the Flags() [OCVTAKEN] bit is set which signals an
initial OCV reading has been taken. For maximum initialization accuracy, any significant charge or
discharge current should be postponed until the ControlStatus() [INITCOMP] bit is set. This could take up
to 10 seconds. After waking, the fuel gauge can proceed with the initialization of the battery information.
During HIBERNATE mode, RAM-based data values are maintained, but gauging status is lost. Upon exit
from HIBERNATE mode, the fuel gauge will immediately reacquire measurements and reinitialize all
gauging predictions


The bq27421-G1D by default is configured to enter HIBERNATE mode in approximately 3 seconds. Other
devices in the bq27421-G1 family are configured by default to enter HIBERNATE mode on the order of
minutes.

a benefit to HIBERNATE mode is that the data RAM values are maintained.

The gauge will enter HIBERNATE mode normally when the following parameters are set to the specified
values:
• Hibernate V = 2200 mV
• FH Setting 0 = 60
• FH Setting 1 = 100
• FH Setting 2 = 18000
• FH Setting 3 = 25

2.4.6.1
Fast HIBERNATE Configuration

The fast HIBERNATE configuration changes Hibernate Voltage to the maximum allowed voltage,
allowing the gauge is enter WAIT_HIBERNATE mode quickly. 



---------
GPOUT Pin
if the bit is set, the Battery
Low Indicator (BAT_LOW) function is selected for the GPOUT pin. If it is cleared, the SOC interrupt
(SOC_INT) function is selected for the GPOUT pin.

Battery Detection (BIN) pin

1) Host drives BIN pin from logic high to low to signal
battery insertion.


SEALED Access ?

--------------------------------
Standard Commands

FullChargeCapacity()// FCC

StateOfHealth()// SOH

4.15 StateOfHealth(): 0x20 and 0x21
0x20 SOH percentage: this read-only function returns an unsigned integer value, expressed as a
percentage of the ratio of predicted FCC(25°C, SOH LoadI) over the DesignCapacity(). 
The FCC(25°C,SOH LoadI) is the calculated FCC at 25°C and the SOH LoadI which is factory programmed (default =–400 mA). 
The range of the returned SOH percentage is 0x00 to 0x64, indicating 0 to 100%,　correspondingly.


RESET 0x0041 No Performs a full device reset
SOFT_RESET 0x0042 No Gauge exits CONFIG UPDATE mode

CHEM_ID: 0x0008
Instructs the fuel gauge to return the chemical identifier for the Impedance TrackTM configuration to
addresses 0x00 and 0x01. The expected value for bq27421-G1A is 0x0128, 0x0312 for bq27421-G1B,
and 0x3142 for bq27421-G1D.

4.1.11 SET_CFGUPDATE: 0x0013
Instructs the fuel gauge to set the Flags() [CFGUPMODE] bit to 1 and enter CONFIG UPDATE mode. This
command is only available when the fuel gauge is UNSEALED.

4.1.13 SHUTDOWN: 0x001C
Instructs the fuel gauge to immediately enter SHUTDOWN mode after receiving this subcommand. The
SHUTDOWN mode is effectively a power-down mode with only a small circuit biased by the BAT pin
which is used for wake-up detection. To enter SHUTDOWN mode, the SHUTDOWN_ENABLE
subcommand must have been previously received. To exit SHUTDOWN mode, the GPOUT pin must be
raised from logic low to logic high for at least 200 μs.


When OpConfig [BIE] is set, [BAT_DET] is set by detecting a logic
high-to-low transition at the BIN pin.

RemainingCapacity(): 0x0C and 0x0D
This read-only command pair returns the remaining battery capacity compensated for load and　temperature. 
If OpConfigB [SMOOTHEN] = 1, this register is equal to RemainingCapacityFiltered();
otherwise, it is equal to RemainingCapacityUnfiltered(). Units are mAh.

filter与unfilter的区别是是否有 SMOOTHEN 还是　filtered compensated for load and　temperature？

4.8
FullChargeCapacity(): 0x0E and 0x0F
This read-only command pair returns the compensated capacity of the battery when fully charged.
FullChargeCapacity() is updated at regular intervals and is compensated for load and temperature. If
OpConfigB [SMOOTHEN] = 1, this register is equal to FullChargeCapacityFiltered(); otherwise, it is equal
to FullChargeCapacityUnfiltered().

4.13 StateOfCharge(): 0x1C and 0x1D
This read-only function returns an unsigned integer value of the predicted remaining battery capacity
expressed as a percentage of FullChargeCapacity(), with a range of 0 to 100%.

RemainingCapacityUnfiltered(): 0x28 and 0x29
This read-only command pair returns the true battery capacity remaining. This value can jump as the
gauge updates its predictions dynamically. Units are mAh.

RemainingCapacityFiltered(): 0x2A and 0x2B
This read-only command pair returns the filtered battery capacity remaining. This value is not allowed to
jump unless RemainingCapacityUnfiltered() reaches empty or full before RemainingCapacityFiltered()
does. Units are mAh.

4.19 FullChargeCapacityFiltered(): 0x2E and 0x2F
This read-only command pair returns the filtered compensated capacity of the battery when fully charged.
Units are mAh. FullChargeCapacityFiltered() is updated at regular intervals. It has no physical meaning
and is manipulated to ensure the StateOfCharge() register is smoothed if OpConfigB [SMOOTHEN] = 1.

4.20 StateOfChargeUnfiltered(): 0x30 and 0x31
This read-only command pair returns the true state-of-charge. Units are %. StateOfChargeUnfiltered() is
updated at regular intervals, and may jump as the gauge updates its predictions dynamically.


NominalAvailableCapacity(): 0x08 and 0x09 ?

spikes //尖峰

4.12 AveragePower(): 0x18 and 0x19
It is negative during discharge and positive during charge. A value of 0
indicates that the battery is not being discharged.



extended commands are not limited to 2-
byte words. The number of command bytes for a given extended command ranges in size from single to
multiple bytes,


6.1.2 Access Modes
The fuel gauge provides two access modes, UNSEALED and SEALED, that control the Data Memory
access permissions. The default access mode of the fuel gauge is UNSEALED, so the system processor
must send a SEALED subcommand after a gauge reset to utilize the data protection feature.


6.3 Data Memory Summary Tables


An over-temperature condition is detected if Temperature() ≥ Over Temp (default = 55 °C) and indicated
by setting the Flags() [OT] bit. The [OT] bit is cleared when Temperature() < Over Temp – Temp Hys
(default = 50 °C).
An under-temperature condition is detected if Temperature() ≤ Under Temp (default = 0 °C) and indicated
by setting the Flags() [UT] bit. The [UT] bit is cleared when Temperature() > Under Temp + Temp Hys
(default = 5 °C).


6.4.1.2.2 Full Charge Set %, Full Charge Clear % 是多少？

6.4.1.5.1 Operation Configuration (OpConfig) Register

6.4.1.6.1 Hibernate Current　３ma(default)
6.4.1.6.2 Hibernate Voltage 2.2v(default)

6.4.2.1.1 Fast Hibernate Settings
6.4.2.1.10 User-Defined Rate-Current?


6.4.2.2
Current Thresholds Subclass

The discharge current threshold can be calculated as Design Capacity / (Dsg Current Threshold × 0.1).
The default is effectively C / 16.7.
The charge current threshold can be calculated as Design Capacity / (Chg Current Threshold × 0.1).
The default is effectively C / 10.
The quit current threshold can be calculated as Design Capacity / (Quit Current × 0.1). The default is
effectively C / 25.

Charge mode is exited and relaxation mode is entered when EffectiveCurrent() goes below the quit
current threshold for the number of seconds specified in Charge Relax Time (default 60 s). Discharge
mode is entered when EffectiveCurrent() goes below the discharge current threshold for Quit Relax Time
(default 1 s). Discharge mode is exited and relaxation mode is entered when EffectiveCurrent() goes
above negative quit current threshold for Dsg Relax Time (default 60 s). Charge mode is entered when
EffectiveCurrent() goes above the charge current threshold for Charge Relax Time (default 60 s).


6.4.2.3.4 Load Select, Load Mode

Load Mode configures the fuel gauge to use either a constant-current or constant-power model for the
Impedance TrackTM algorithm. When Load Mode is 0, the Constant Current Model is used. When Load
Mode is 1 (default), the Constant Power Model is used.

Qmax??

6.4.2.3.6 Design Capacity, Design Energy, Default Design Capacity
