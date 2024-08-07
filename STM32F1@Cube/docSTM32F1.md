# STM32F1 Project Setup Document

- ## MCU Board
    - STM32 serial: **STM32F103C8T6**
  
    ![F1-Board.png](../Document/Image/F1-Board.png)
  
- ## CubeMX Setup
    - ### Select MCU by part No.
      ![F1-MCU.png](../Document/Image/F1-MCU.png) 
  
    - ### Clock Tree setup
      - #### Pinout & Configuration / System Core / RCC
      ![F1-RCC.png](../Document/Image/F1-RCC.png) 
      - #### Clock Configuration
      ![F1-Clock.png](../Document/Image/F1-Clock.png)

    - ### GPIOs
      - #### LCD reset pin - PB6
      ![F1-GPIO1.png](../Document/Image/F1-GPIO1.png)
      - #### On board LED pin - PA8
      ![F1-GPIO2.png](../Document/Image/F1-GPIO2.png)
  
    - ### TIM use channel 1
      ![F1-TIM1.png](../Document/Image/F1-TIM1.png) 

    - ### SPI use channel 1
      ![F1-SPI.png](../Document/Image/F1-SPI.png)

    - ### UART use channel 3
      ![F1-UART.png](../Document/Image/F1-UART.png)
    
    - ### NVIC Setting
      ![F1-NVIC.png](../Document/Image/F1-NVIC.png)
    
    - ### IC Pin setting overview
      ![F1-IC.png](../Document/Image/F1-IC.png)

    - ### Final project setting. Use Makefile to generate project code
      ![F1-Project.png](../Document/Image/F1-Project.png)

- ## Wiring
    - ### Connect w/ LCD
    ![F1-LCD.png](../Document/Image/F1-LCD.png)

    - ### Connect w/ PC
    ![F1-PC.png](../Document/Image/F1-PC.png)

- ## Build and download to board
    - ### Make sure you have required build environment
        - [OpenOCD](https://openocd.org)
        - [GNU Arm Embedded Toolchain](https://developer.arm.com/downloads/-/gnu-rm)
        - [Using GCC with MinGW on VScode](https://code.visualstudio.com/docs/cpp/config-mingw)
    - ### Using vscode task function at vscode
    ![vscode-task.png](../Document/Image/vscode-task.png)
    - ### Run "build" to start build binary file. Run "download" to download to board
    ![vscode-option.png](../Document/Image/vscode-option.png)
    - ### Can setting task content at .vscode/tasks.json
    ![vscode-json.png](../Document/Image/vscode-json.png)

- ## Finally. Display bad apple
   ### 1. Choose python script, 5 FPS or 10 FPS frame size
   ### 2. Select board type and serial com port on your computer
    ```
    # Function by board type
    board_list = ["STM32F1", "other"]
    board_type = board_list[0]
    
    # Init Serial
    port = "COM3"
    ser = serial.Serial(port, baudrate=460800, bytesize=8, parity=serial.PARITY_NONE, stopbits=1)
    ```
   ### 3. Start python script
   ### 4. Power on your board
   ### 5. 🎉 You can see Bad apple on LCD!!! 🎉
