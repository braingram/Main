################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../../../../../makefile.local

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS_QUOTED += \
"E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/http_server.c" \

C_SRCS += \
E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/http_server.c \

OBJS += \
./Sources/Applications/Web\ Server/HTTP/HTTP\ Server/http_server_c.obj \

OBJS_QUOTED += \
"./Sources/Applications/Web Server/HTTP/HTTP Server/http_server_c.obj" \

C_DEPS += \
./Sources/Applications/Web\ Server/HTTP/HTTP\ Server/http_server_c.d \

OBJS_OS_FORMAT += \
./Sources/Applications/Web\ Server/HTTP/HTTP\ Server/http_server_c.obj \

C_DEPS_QUOTED += \
"./Sources/Applications/Web Server/HTTP/HTTP Server/http_server_c.d" \


# Each subdirectory must supply rules for building sources it contributes
Sources/Applications/Web\ Server/HTTP/HTTP\ Server/http_server_c.obj: E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/http_server.c
	@echo 'Building file: $<'
	@echo 'Executing target #87 $<'
	@echo 'Invoking: ColdFire Compiler'
	"$(CF_ToolsDirEnv)/mwccmcf" @@"Sources/Applications/Web Server/HTTP/HTTP Server/http_server.args" -o "Sources/Applications/Web Server/HTTP/HTTP Server/http_server_c.obj" "$<" -MD -gccdep
	@echo 'Finished building: $<'
	@echo ' '

Sources/Applications/Web\ Server/HTTP/HTTP\ Server/http_server_c.d: E:/Main/Firmware/BaseEthernetNode/Sources/APPLICATIONS/WEB/http_server.c
	@echo 'Regenerating dependency file: $@'
	
	@echo ' '


