from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

# Fungsi untuk mengubah mode penerbangan
def set_flight_mode(vehicle, mode):
    while vehicle.mode != VehicleMode(mode):
        vehicle.mode = VehicleMode(mode)
        time.sleep(1)

# Fungsi untuk melakukan manuver ekstrem hingga 90 derajat
def perform_extreme_maneuver(vehicle):
    print("Memulai manuver ekstrem")

    # Menggerakkan drone sejauh 90 derajat
    heading_target = vehicle.heading + 90
    vehicle.simple_goto(LocationGlobalRelative(vehicle.location.global_frame.lat,
                                                vehicle.location.global_frame.lon,
                                                vehicle.location.global_frame.alt),
                        groundspeed=10,
                        heading=heading_target)
    
    while abs(vehicle.heading - heading_target) > 5:
        time.sleep(1)

    print("Manuver ekstrem selesai")

# Menghubungkan ke drone
connection_string = 'udp:127.0.0.1:14550'  # Sesuaikan dengan koneksi drone Anda
vehicle = connect(connection_string, wait_ready=True)

try:
    # Mengganti mode ke GUIDED
    set_flight_mode(vehicle, 'GUIDED')

    # Menunggu hingga drone siap
    while not vehicle.is_armable:
        time.sleep(1)

    # Mengaktifkan motor
    vehicle.armed = True
    time.sleep(2)

    # Mengambil kendali
    set_flight_mode(vehicle, 'GUIDED')

    # Memulai manuver ekstrem
    perform_extreme_maneuver(vehicle)

    # Menetapkan titik target untuk mendarat
    target_location = LocationGlobalRelative(-34.364114, 149.166022, 30)  # Ganti dengan koordinat target Anda

    # Pendaratan pada titik target
    vehicle.simple_goto(target_location)
    while vehicle.location.global_relative_frame.alt > 1:
        time.sleep(1)

except Exception as e:
    print(f"Terjadi kesalahan: {e}")

finally:
    # Mendaratkan drone dan menonaktifkan motor saat program selesai
    set_flight_mode(vehicle, 'LAND')
    vehicle.armed = False

    # Tutup koneksi
    vehicle.close()
