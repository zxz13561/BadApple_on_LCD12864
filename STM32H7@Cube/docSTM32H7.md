# STM32H7 Project Setup Document

- ## MCU Board
    - STM32 serial: **STM32H753ZI**
    - It is almost same as H743 version
      
    ![H7-Board.png](../Document/Image/H7-Board.png)
  
- ## CubeMX Setup
    - ### Select MCU by part No.
      ![H7-MCU.png](../Document/Image/H7-MCU.png) 
  
    - ### Clock Tree setup
      - #### Pinout & Configuration / System Core / RCC
      ![H7-RCC.png](../Document/Image/H7-RCC.png) 
      - #### Clock Configuration
      ![H7-Clock.png](../Document/Image/H7-Clock.png)
  
    - ### TIM use channel 1
      ![H7-TIM.png](../Document/Image/H7-TIM.png) 

    - ### SPI use channel 1
      ![H7-SPI.png](../Document/Image/H7-SPI.png)
    
    - ### Setup UART pins
      ![H7-UART-Pin.png](../Document/Image/H7-UART-Pin.png)
  
    - ### UART use channel 3
      ![H7-UART.png](../Document/Image/H7-UART.png)
    
    - ### NVIC Setting
      ![H7-NVIC.png](../Document/Image/H7-NVIC.png)

    - ### Final project setting. Use Makefile to generate project code
      ![H7-Project.png](../Document/Image/H7-Project.png)

  - ## Wiring
      - ### Connect w/ LCD
      ![H7-LCD.png](../Document/Image/H7-LCD.png)

      - ### Connect w/ PC
      ![H7-PC.png](../Document/Image/H7-PC.png)

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
    board_type = board_list[1]
    
    # Init Serial
    port = "COM3"
    ser = serial.Serial(port, baudrate=460800, bytesize=8, parity=serial.PARITY_NONE, stopbits=1)
    ```
   ### 3. Start python script
   ### 4. Power on your board
   ### 5. 🎉 You can see Bad apple on LCD!!! 🎉
