################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"E:/Main/Firmware/BaseEthernetNode/Sources/HIL/High Level Drivers/SPI/spi_rtos.c" \

C_SRCS += \
E:/Main/Firmware/BaseEthernetNode/Sources/HIL/High\ Level\ Drivers/SPI/spi_rtos.c \

OBJS += \
./Sources/HIL/High\ Level\ Drivers/SPI/spi_rtos_c.obj \

OBJS_QUOTED += \
"./Sources/HIL/High Level Drivers/SPI/spi_rtos_c.obj" \

C_DEPS += \
./Sources/HIL/High\ Level\ Drivers/SPI/spi_rtos_c.d \

OBJS_OS_FORMAT += \
./Sources/HIL/High\ Level\ Drivers/SPI/spi_rtos_c.obj \

C_DEPS_QUOTED += \
"./Sources/HIL/High Level Drivers/SPI/spi_rtos_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/HIL/High\ Level\ Drivers/SPI/spi_rtos_c.obj: E:/Main/Firmware/BaseEthernetNode/Sources/HIL/High\ Level\ Drivers/SPI/spi_rtos.c
	@echo 'Building file: $<'
	@echo 'Executing target #68 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/HIL/High Level Drivers/SPI/spi_rtos.args" -o "Sources/HIL/High Level Drivers/SPI/spi_rtos_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/HIL/High\ Level\ Drivers/SPI/spi_rtos_c.d: E:/Main/Firmware/BaseEthernetNode/Sources/HIL/High\ Level\ Drivers/SPI/spi_rtos.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


