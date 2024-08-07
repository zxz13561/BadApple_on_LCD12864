# STM32F1 Project Setup Document

---

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