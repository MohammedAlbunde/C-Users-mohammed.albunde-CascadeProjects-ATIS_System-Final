# ATIS Pro Connection Diagram

```mermaid
graph TB
    subgraph AWOS ["Vaisala AWOS System"]
        AWOS_MAIN["Main AWOS Unit"]
        WIND["Wind Sensor"]
        TEMP["Temp/Humidity"]
        VIS["Visibility Sensor"]
        RVR["RVR Sensor"]
        
        WIND --> AWOS_MAIN
        TEMP --> AWOS_MAIN
        VIS --> AWOS_MAIN
        RVR --> AWOS_MAIN
    end

    subgraph COMPUTER ["ATIS Pro Computer"]
        CPU["PC (Core i5/i7)"]
        AUDIO["Audio Interface"]
        NET["Network Card"]
        SERIAL["Serial Ports"]
        UPS["UPS Power"]
        
        NET --> CPU
        AUDIO --> CPU
        SERIAL --> CPU
        UPS --> CPU
    end

    subgraph RADIO ["VHF Radio System"]
        VHF["VHF Transmitter"]
        PTT["PTT Control"]
        ANT["Antenna"]
        
        PTT --> VHF
        VHF --> ANT
    end

    %% Connections
    AWOS_MAIN -->|"Ethernet\n192.168.1.x"| NET
    AUDIO -->|"Audio Out\n3.5mm"| VHF
    SERIAL -->|"RS-232\nCOM1"| PTT

    %% Power Connections
    POWER["Main Power\n220V/50Hz"] --> UPS
    UPS -->|"Clean Power"| VHF
```

## Physical Connections

### 1. AWOS Connections
```
[Vaisala AWOS] ───────────────────────► [Computer]
    │                                       │
    └─► Network Port 1 ──► CAT6 Cable ──►  │
    └─► Serial Port (backup) ──► RS-232 ─►  │
```

### 2. Audio Connections
```
[Computer] ─────────────────────────► [VHF Radio]
    │                                     │
    └─► Audio Out ──► Audio Cable ──►    │
    └─► Serial Port ──► PTT Cable ──►    │
```

### 3. Power Connections
```
[Main Power 220V] ──► [UPS] ──┬──► [Computer]
                              ├──► [VHF Radio]
                              └──► [Network Switch]
```

## Port Assignments

### Computer Ports
1. **Network Ports**
   - ETH0: AWOS Connection (192.168.1.100)
   - ETH1: Airport Network (Optional)

2. **Serial Ports**
   - COM1: VHF Radio PTT
   - COM2: Backup AWOS (Optional)

3. **Audio Ports**
   - Line Out: VHF Radio Input
   - Line In: Test/Monitor (Optional)

### Cable Types

1. **Network Cables**
   - Type: CAT6 Shielded
   - Length: 10m (customize as needed)
   - Connectors: RJ45 with boots

2. **Serial Cables**
   - Type: RS-232
   - Length: 3m
   - Connectors: DB9 Male/Female

3. **Audio Cables**
   - Type: Balanced Audio
   - Length: 2m
   - Connectors: XLR or 1/4" TRS

## Grounding Requirements

1. **Equipment Grounding**
   ```
   [Ground Point] ──┬──► [Computer]
                    ├──► [VHF Radio]
                    ├──► [UPS]
                    └──► [Network Switch]
   ```

2. **Lightning Protection**
   ```
   [Lightning Arrestor] ──┬──► [Network Lines]
                         └──► [Power Lines]
   ```

## Power Requirements

1. **UPS Specifications**
   - Capacity: 2000VA
   - Runtime: 30 minutes
   - Input: 220V/50Hz
   - Output: Pure Sine Wave

2. **Power Distribution**
   ```
   [UPS] ──┬──► [Computer] (500W)
           ├──► [VHF Radio] (200W)
           └──► [Network Switch] (50W)
   ```

## Safety Notes

1. **Electrical Safety**
   - All power connections must be grounded
   - Use surge protectors
   - Label all cables
   - Keep documentation of connections

2. **Maintenance Access**
   - Leave 1m clearance for maintenance
   - Label all connection points
   - Document any changes
   - Keep spare cables on hand
