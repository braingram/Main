################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"/home/jwhong/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/FLASH/flash.c" 

C_SRCS += \
/home/jwhong/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/FLASH/flash.c 

OBJS += \
./Sources/HAL/FLASH/flash_c.obj 

OBJS_QUOTED += \
"./Sources/HAL/FLASH/flash_c.obj" 

C_DEPS += \
./Sources/HAL/FLASH/flash_c.d 

OBJS_OS_FORMAT += \
./Sources/HAL/FLASH/flash_c.obj 

C_DEPS_QUOTED += \
"./Sources/HAL/FLASH/flash_c.d" 


# Each subdirectory must supply rules for building sources it contributes
Sources/HAL/FLASH/flash_c.obj: /home/jwhong/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/FLASH/flash.c
	@echo 'Building file: $<'
	@echo 'Executing target #8 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HAL/FLASH/flash.args" -o "Sources/HAL/FLASH/flash_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HAL/FLASH/flash_c.d: /home/jwhong/Project-Hexapod/Firmware/BaseEthernetNode/Sources/HAL/mcf51cn128/drivers/FLASH/flash.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '

