################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/DHCP Client/dhcp_app.c" \

C_SRCS += \
E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/DHCP\ Client/dhcp_app.c \

OBJS += \
./Sources/Applications/DHCP\ Client/dhcp_app_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/DHCP Client/dhcp_app_c.obj" \

C_DEPS += \
./Sources/Applications/DHCP\ Client/dhcp_app_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/DHCP\ Client/dhcp_app_c.obj \

C_DEPS_QUOTED += \
"./Sources/Applications/DHCP Client/dhcp_app_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/DHCP\ Client/dhcp_app_c.obj: E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/DHCP\ Client/dhcp_app.c
	@echo 'Building file: $<'
	@echo 'Executing target #91 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/DHCP Client/dhcp_app.args" -o "Sources/Applications/DHCP Client/dhcp_app_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/DHCP\ Client/dhcp_app_c.d: E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/DHCP\ Client/dhcp_app.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


