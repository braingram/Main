################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"E:/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/GPIO/gpio.c" \

C_SRCS += \
E:/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/GPIO/gpio.c \

OBJS += \
./Sources/HAL/GPIO/gpio_c.obj \

OBJS_QUOTED += \
"./Sources/HAL/GPIO/gpio_c.obj" \

C_DEPS += \
./Sources/HAL/GPIO/gpio_c.d \

OBJS_OS_FORMAT += \
./Sources/HAL/GPIO/gpio_c.obj \

C_DEPS_QUOTED += \
"./Sources/HAL/GPIO/gpio_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/HAL/GPIO/gpio_c.obj: E:/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/GPIO/gpio.c
	@echo 'Building file: $<'
	@echo 'Executing target #80 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HAL/GPIO/gpio.args" -o "Sources/HAL/GPIO/gpio_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HAL/GPIO/gpio_c.d: E:/Main/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/GPIO/gpio.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


