# Connection Notes

Service UUID: 0000ff00-0000-1000-8000-00805f9b34fb

(BLEDevice(C84441EE-5C57-2681-1BD5-82AF18C58F5D, Leviton DD710), AdvertisementData(local_name='Leviton DD710 V6.4', manufacturer_data={1468: b'\x002\x00'}, service_uuids=['0000ff00-0000-1000-8000-00805f9b34fb'], tx_power=0, rssi=-79))
(BLEDevice(A6F62C23-42EB-0659-242B-8AB323888675, Leviton DDS15 V6.6), AdvertisementData(local_name='Leviton DDS15 V6.6', manufacturer_data={1468: b'\x01d\x00'}, service_uuids=['0000ff00-0000-1000-8000-00805f9b34fb'], tx_power=0, rssi=-84))

## Connection

### Connection packet bytes

0000 44 35 00 03 ec d5 02 0a 01 27 25 00 00 23 52 7a D5.......'%..#Rz
0010 d0 d6 be 89 8e 45 22 eb 6b 07 46 d4 53 3f 03 3e .....E".k.F.S?.>
0020 b5 14 34 5d ac 9a af 00 57 41 03 14 00 18 00 00 ..4]....WA......
0030 00 48 00 fb 07 00 00 00 27 d3 cd 1f .H......'...

0000 10 21 00 03 cc c4 06 0a 03 0a 1f 22 00 9f 95 d1 .!........."....
0010 c4 57 5a 65 50 02 0e 0a 00 04 00 12 37 00 11 53 .WZeP.......7..S
0020 8c 4c 89 fa a5 a2 45 ef .L....E.

Potential key:
8c 4c 89 fa a5

0x8c4c89faa5

### Turning Lights on from phone (worked)

Write data from phone:

3752 14.710 Master_0xaf9a82d3 LE 1M ATT 9 89690µs 0 0 False 201 Sent Write Request, Handle: 0x0025 (Unknown: Unknown)
0000 20 1c 00 03 4e 99 06 0a 03 03 1e c9 00 ff e4 e2 ...N...........
0010 09 d3 82 9a af 02 09 05 00 04 00 12 25 00 01 63 ............%..c
0020 a8 68 31 .h1

Value changed notification:

3755 14.800 Slave_0xaf9a82d3 LE 1M ATT 9 151µs 1 0 True 202 Rcvd Handle Value Notification, Handle: 0x0025 (Unknown: Unknown)
0000 20 1c 00 03 51 99 06 0a 01 0b 40 ca 00 77 45 e4 ...Q.....@..wE.
0010 09 d3 82 9a af 1a 09 05 00 04 00 1b 25 00 01 63 ............%..c
0020 cc 4e a8 .N.

Write response from device:

3757 14.801 Slave_0xaf9a82d3 LE 1M ATT 5 151µs 0 1 False 202 Rcvd Write Response, Handle: 0x0025 (Unknown: Unknown)
0000 20 18 00 03 53 99 06 0a 01 0b 40 ca 00 8c 47 e4 ...S.....@...G.
0010 09 d3 82 9a af 06 05 01 00 04 00 13 09 c7 1c ...............

## Characteristics

INFO:decora_bleak.decora_bleak:SERVICE: Vendor specific

state
INFO:decora_bleak.decora_bleak: characteristic: 0000ff01-0000-1000-8000-00805f9b34fb 36 Vendor specific ['read', 'write', 'notify']
INFO:decora_bleak.decora_bleak: descriptor: 38 Client Characteristic Configuration
INFO:decora_bleak.decora_bleak: descriptor: 39 Characteristic User Description

config1
INFO:decora_bleak.decora_bleak: characteristic: 0000ff02-0000-1000-8000-00805f9b34fb 40 Vendor specific ['read', 'write', 'notify']
INFO:decora_bleak.decora_bleak: descriptor: 42 Client Characteristic Configuration
INFO:decora_bleak.decora_bleak: descriptor: 43 Characteristic User Description

config2
INFO:decora_bleak.decora_bleak: characteristic: 0000ff03-0000-1000-8000-00805f9b34fb 44 Vendor specific ['read', 'write', 'notify']
INFO:decora_bleak.decora_bleak: descriptor: 46 Client Characteristic Configuration
INFO:decora_bleak.decora_bleak: descriptor: 47 Characteristic User Description

location1
INFO:decora_bleak.decora_bleak: characteristic: 0000ff04-0000-1000-8000-00805f9b34fb 48 Vendor specific ['read', 'write']
INFO:decora_bleak.decora_bleak: descriptor: 50 Characteristic User Description
bytearray(b'&z\x00\x00')

location2
INFO:decora_bleak.decora_bleak: characteristic: 0000ff05-0000-1000-8000-00805f9b34fb 51 Vendor specific ['read', 'write']
INFO:decora_bleak.decora_bleak: descriptor: 53 Characteristic User Description
bytearray(b'\x08\x00\x01\x00')

event
INFO:decora_bleak.decora_bleak: characteristic: 0000ff06-0000-1000-8000-00805f9b34fb 54 Vendor specific ['read', 'write']
INFO:decora_bleak.decora_bleak: descriptor: 56 Characteristic User Description
bytearray(b'LEVITON')

time
INFO:decora_bleak.decora_bleak: characteristic: 0000ff07-0000-1000-8000-00805f9b34fb 57 Vendor specific ['read', 'write']
INFO:decora_bleak.decora_bleak: descriptor: 59 Characteristic User Description
bytearray(b'\x15#,')

data
INFO:decora_bleak.decora_bleak: characteristic: 0000ff08-0000-1000-8000-00805f9b34fb 60 Vendor specific ['read', 'write']
INFO:decora_bleak.decora_bleak: descriptor: 62 Characteristic User Description
bytearray(b'\xe7\x07\x07\n')

name
INFO:decora_bleak.decora_bleak: characteristic: 0000ff09-0000-1000-8000-00805f9b34fb 63 Vendor specific ['read', 'write']
INFO:decora_bleak.decora_bleak: descriptor: 65 Characteristic User Description
bytearray(b'Garage\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
