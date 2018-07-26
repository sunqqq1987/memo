==========基本概念================

Hi-Z: 高阻, 它表示没有任何驱动的输出信号状态，该信号处于开路状态，既不是高电平也不是低电平。
电路分析时高阻态可做开路理解。你可以把它看作输出（输入）电阻非常大。他的极限可以认为悬空。

latched： 被锁定
trip points:跳闸点
lbc:  linear battery charger
inhibit: 抑制
taper: 逐渐变细

“Wall adapter” (dedicated charging port)

Automatic Power Source Detection (APSD) algorithm

four power source types that are detected are:
1. Standard Downstream Port (SDP) //limited to 100 mA
2. Charging Downstream Port (CDP) //higher than 500 mA
3. Dedicated Charging Port (DCP)  //higher than 500 mA
4. Other charging port (not covered by USB charging specification 1.1)


battery drain 电池耗竭，即soc=0 了

OCV是Open circuit voltage=开路电压,指的是电池不放电开路时,两极之间的电位差


1、电池容量　　
电池的容量由电池内活性物质的数量决定，通常用毫安时mAh或者 Ah表示。例如1000 mAh就是能以1 A的电流放电1 h换算为所含电荷量大约为3600 C。　　

2、标称电压　　
电池正负极之间的电势差称为电池的标称电压。标称电压由极板材料的电极电位和内部电解液的浓度决定。
锂电放电图，是呈抛物线的，4.3V降到3.7V和3.7V降到3.0V，都是变化很快的。惟有3.7V左右的放电时间是最长的，几乎占到了3/4的时间，因此锂电池的标称电压是指维持放电时间最长的那段电压。
锂电池的标称电压有3.7V和3.8V，如果为3.7V，则充电终止电压为4.2V，如果为3.8V，则充电终止电压为4.35V。

3、充电终止电压　　
可充电电池充足电时，极板上的活性物质已达到饱和状态，再继续充电，电池的电压也不会上升，此时的电压称为充电终止电压。锂离子电池为4.2 V或者4.35V。　　

4、放电终止电压　　
放电终止电压是指蓄电池放电时允许的最低电压。放电终止电压和放电率有关。一般来讲单元锂离子电池为2.7 V。　

5、电池内阻　　
电池的内阻由极板的电阻和离子流的阻抗决定，在充放电过程中，图像引擎以及极板的电阻是不变的，但离子流的阻抗将随电解液浓度和带电离子的增减而变化。
当锂电池的OCV电压降低时，阻抗会增大，因此在低电（小于3V）充电时，要先进行预充电（涓流充电），防止电流太大引起电池发热量过大。

6、自放电率　　
是指在一段时间内，电池在没有使用的情况下，自动损失的电量占总容量的百分比。一般在常温下锂离子电池自放电率为5%-8%。


以600mAh的电池为例，设置截至电流为0.01C(即6mA)

==========================================
bugreport里的battery信息：
找　DUMP OF SERVICE battery

==========SMB23X===========================

VIN = input (adapter or USB port) voltage
VBATT = battery voltage
VSYS = system voltage
IOUT = charge current
ISYS = system current

Voltage Mode Battery Monitoring System (VM-BMS)

Battery charging current during ATC (auto-trickle-charge) phase A using the linear trickle charger
Battery charging current during ATC (auto-trickle-charge) phase B using the switch-mode charger


When the input adapter is not present or when the current required by the system is higher than the programmed input current
limit, the system output (SYS) is connected to the battery output (OUT) through an internal 40 mΩ system load switch.

When a valid adapter voltage is present at IN, the system voltage can either be regulated to 4.3 V, 5.5 V, 
or directly use the voltage present at the input (programmable option).


Auto-Power Source Detection(APSD) Enabled ?

INOK interrupt is used to indicate valid input adapter presence,
enable it in suspend to make sure USB insertion and removal could be detected after device suspended.

-----------charging------------

The SMB23x family uses the D+ and D- USB lines to determine the type of charger dedicated to the handheld device and
automatically adjust charge current based on the power source type.

0. pre-qualification check

When an external supply is inserted and the EN input is asserted, the SMB23x family performs
the pre-qualification checks before initiating a charging cycle. The input voltage needs to be
higher than the UVLO threshold and the cell temperature needs to be within the temperature
limits for the charging cycle to start.

For supporting USB compliancy, the SMB23x family defaults to the USB1 mode for
approximately 120 msec after valid input power is applied.


1. 涓流充电

//Trickle charge current(30ma~25ma) versus battery voltage(1v~2v)

datasheet: 充电电流典型值22ma(V_BATT=1.8V时,电压２.05v(typ.)), 现在设置的充电电流多少？90ma

If the battery voltage is below 2.1 V (trickle-charge to pre-charge threshold), the device will
apply a trickle-charge current of 22 mA (typical). This allows the SMB23x family to reset the
protection circuit in the battery pack and bring the battery voltage to a higher level without　compromising safety

有个pre-charge timer, 在这个timer周期内必须到达pre-charge的电压.如果没有达到则发生错误
If the trickle-charge to pre-charge voltage threshold is not exceeded before the pre-charge timer expires, 
the charge cycle is terminated, both FETs are turned off and power recycling is necessary for re-initiating charging.

在datasheet中有： Pre-charge timeout (includes trickle charging), 45 min


2. 进入pre-charge的阈值是2.2v(选择），(2.05v(typ), data sheet)

datasheet: pre-charge电压的４个级别：2.5,2.6,2.8,3.0v，对应的pre-charge电流：20ma（选择？）,30ma,50ma,75ma

The preconditioning current is programmable, with the default value at C/10.
If the battery voltage does not reach the preconditioning voltage level (programmable) within a
specified amount of time (pre-charge timeout), the safety timer expires and the charge cycle is　terminated
=>pre-charge timer内确保会升到fast-charge的阈值

-------8x10-----[
CHGR_VBAT_TRKL //address 0x1050, 可设的pre charge电压范围：2.05～2.8v
Battery voltage threshold for trickle charging; below which the battery is charged with the linear trickle charger with IBAT_TRKL_A
V = 2.05 V + X * 50 mV, X = 0, 1, , 15
2.05： PM_CHG_VBAT_TRKL_MIN_THRESHOLD
当前sbl设置的是： PM_CHG_FLCB_DEAD_BATTERY_THRESHOLD


CHGR_VBAT_WEAK //address 0x1052, 可设的fast-charge电压范围：2.1～3.6v
Weak battery voltage threshold; above which system can boot, and fast charging can start
V = 2.1 V + X * 100 mV, X = 0, ... ,15
2.1： PM_CHG_VBAT_WEAK_MIN_THRESHOLD
3.6： PM_CHG_VBAT_WEAK_MAX_THRESHOLD
当前sbl设置的是：PM_CHG_FLCB_WEAK_BATTERY_THRESHOLD
---------------]

3. 进入fast-charge的阈值是3.0v，然后进行恒流充电，直到到达float volatage（4.4v, 可选范围有(3.48,...,4.72))

datasheet: 对应的充电电流有 100,250,300ma（选择）,370,600,700,1000ma

fast charge timer是 180 min(选择),270,360 (见datasheet中 Complete-charge timeout)

When the battery voltage reaches the pre-charge to fast-charge voltage level, the SMB23x family
enters the constant current (fast charge) mode. The fast charge current level is programmable via　the corresponding register.


4. 到达float voltage后，进入恒压充电（保持电池的电压恒定），之后充电电流会逐渐减小。
恒压充电的模式的终止发生在以下２个条件之一：
１）fast-charge的timer到期（此时异常，因为期望是在该timer内电流降到截止电流）
２）fast-charge的timer没有到期，但充电电流I_CHG降到截止电路的阈值I_TERM（termination current threshold），此时进入停止充电,standby mode

The constant-voltage charging mode will continue until the charge current
drops below the termination current threshold, or until the fast charge timer has expired.

5. re-charge
re-charge电压阈值是？ datasheet: 90mv~200mv, 150mv(typ)

After the charge cycle has terminated, the SMB23x family continues to monitor the battery　voltage. 
If the battery voltage falls below the recharge threshold (programmable), 
the SMB23x family can automatically top-off the battery ？

-----------参数-------------------------------

------DC operating characteristics-

Input Current Limit Mode(ICL 输入电流限制模式)：设定的范围是100ma~1500ma

    USB2.0时，
    USB1: 通过usb进行最大１００ma的充电.　datasheet:80ma~100ma, ９０（typ)
    USB5: 对应最大５００ma. datasheet:  475ma(typ)或275ma(typ)
    
    USB3.0时，
    INUSB1.5: 135ma(typ)
    INUSB9: 860ma(typ)


    AC充电: 指(AICL Algorithm　or Default Setting): 充电电流９０ma～１０００ma
    充电器输入是交流电,输出是直流电

    //see Table 5-1 Configuration register
    Max AC input current limit(I_INLIMIT): 100,300,500, 650, 900, 1000, 1500MA, no limit
    Max USB5 input current limit: 500MA,300MA


I_TERM(Charge termination current range): Four steps， 20 mA, 30 mA, 50 mA, 75 mA

V_SYS（System output voltage）： 4 options，4.20～4.40，.., V_IN, V_BATT + 250 mV(选择)

UVLO threshold (<3.5v)
ovlo threshold (>6.2v)

V_LOWBATT: 15 steps, battery voltage falling, 2.5~3.7v

parameters can also be programmed statically via a user-friendly GUI interface:
■ Battery (float) voltage
■ Fast charge current
■ Pre- to fast-charge voltage threshold
■ Pre-charge current
■ Input current limit
■ Termination current
■ Safety charge timers
■ Battery pack temperature

------AC operating characteristics--

tAICL: AICL delay
tPCTO: Pre-charge timeout = 45 min
tFCTO: Complete-charge timeout

--------------------notes-------------------

When Automatic Power Source Detection is used and a USB port is detected, the current is
automatically limited to 90mA until the system selects transition to the USB5 mode via an I 2 C command
or the corresponding USB1/5 input pin. When USB5 mode is selected, the current is limited by bit[7].
When Automatic Power Source Detection is used and an AC/DC power source is detected, the current
is limited by bits [5:2].

During a battery overvoltage condition, charging is NOT resumed when battery voltage falls below the
battery OVLO threshold (plus hysteresis). Instead, charging needs to be re-enabled for the charging
process to resume.

When battery track system voltage option is selected, low battery detection mode also needs to be enabled.

The devices are in a hold-off status when charging is paused. The conditions that cause or sustain hold-off are the following ones: 
a) internal temperature limit hit, 
b) hot or cold hard limit, 
c) battery voltage less than 2.0 V, 
d) thermistor battery missing (if enabled), 
e) battery voltage not below float voltage by more than the programmed VCH threshold for charge initiation (if enabled), 
f) input under- or overvoltage, suspend mode


----------pins------------------------

INOK output: indicate valid input adapter presence (V_IN > V_UVLO , V_IN < V_OVLO ).

SUSP is a logic input pin for turning on/off the device’s operation (including I 2 C interface)

FET: ?

----------------

Battery standby current（３５ua~40ua) versus battery voltage(2.8v~4.2v)

Shutdown current(8~10ua) versus battery voltage (2.8v~4.2v)

USB input current limit(480ma~475ma) versus battery voltage(2.6v~4.2v)

Input current (900 mA) versus battery voltage(2.5v~3.7v)


--------------------------------
搜“Battery charger”

-------------------AICL-----------------------------
AICL(Auto Input Current Limited)

自动输入电流限制的功能能够根据输入电源的能够提供的最大电流选择充电电流，能够将USB/AC/DC充电器相容。

充电芯片设定一个充电输入门限电压值，比如4.75V，当充电芯片的输入电压大于该门限电压值时，来设置充电电流：
当输入电压没有下降或是稍有下降但高于该门限电压值时，每次以１OOmA逐级提高充电器的输出电流，检测充电芯片的输入电压是否小于门限电压值（每次时间间隔为5--10ms），直到充电芯片的输入电压值小于门限电压值；
设定充电电流为前面一级或前面两级较小电流进行充电，输入电压没有下降到该门限电压值，就以设定好的充电电流进行充电。保证以最大的充电时间，最小的时间完成电池充电。提高用户体验。

AICL = Automatic Input Current Limit　//自动输入电流限制
V_IN = Input Voltage　//输入电压
V_CL = Current Limit Threshold //　充电芯片的限压
I_INACTUAL = Actual Input Current Limit　//实际的限流
I_INLIMIT = Programmed Input Current Limit　//充电芯片的输入电流限制


------------------battery missing检查----------------

Once the BATT pin has reached 2.1 V, the OUT pin will begin charging the BATT pin with the programmed pre-charge
current and the battery missing timer will begin. 
If the BATT pin is charged up above the “missing battery” voltage level before the expiration of the battery missing timer, 
the SMB23x family will assert the missing battery status flag and the IRQ (if enabled).


-----------------Enabling/disabling charging-------
When the charger is disabled, the FET connecting the system (SYS) to the battery (OUT) will remain on.


---------------thermal monitor---------------
If the temperature limits are exceeded, battery charging will be suspended and
safety timers maintain their values but are paused. During this mode, the FET between the battery
and the system is turned on for the system to be powered by the battery. Charging is
automatically re-enabled, the corresponding fault bit is reset, and safety timers continue counting
once temperature level has returned within the safe operating range(with some hysteresis).

A device option also exists for notifying the system of a battery thermal condition, without suspending battery charging.





