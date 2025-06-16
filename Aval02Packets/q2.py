#!/usr/bin/env python3

import os
import sys
import subprocess
import struct

def analisar_imagem(nome_arquivo):
    try:
        with open(nome_arquivo, 'rb') as arquivo:
            if arquivo.read(2) != b'\xff\xd8':
                print("Erro: O arquivo não parece ser uma imagem JPEG válida.")
                return None

            while True:
                marker = arquivo.read(2)
                if not marker:
                    break
                
                if marker == b'\xff\xe1':
                    break
                elif marker[0] == 0xff:
                    tamanho = int.from_bytes(arquivo.read(2), 'big')
                    arquivo.seek(tamanho - 2, 1)
                else:
                    break

            if not marker or marker != b'\xff\xe1':
                print("Erro: Segmento EXIF não encontrado na imagem.")
                return None

            tamanho_app1 = int.from_bytes(arquivo.read(2), 'big') - 2
            dados_app1 = arquivo.read(tamanho_app1)

            if not dados_app1.startswith(b'Exif\x00\x00'):
                print("Erro: Dados EXIF inválidos.")
                return None

            tiff_header = dados_app1[6:]
            byte_order = '>' if tiff_header[0] == 0x4D else '<'

            ifd_offset = struct.unpack(byte_order + 'I', tiff_header[4:8])[0]
            ifd_data = tiff_header[ifd_offset:]

            num_entradas = struct.unpack(byte_order + 'H', ifd_data[:2])[0]
            gps_offset = None

            for i in range(num_entradas):
                entry_offset = 2 + i * 12
                tag = struct.unpack(byte_order + 'H', ifd_data[entry_offset:entry_offset+2])[0]
                
                if tag == 0x8825:
                    gps_offset = struct.unpack(byte_order + 'I', ifd_data[entry_offset+8:entry_offset+12])[0]
                    break

            if not gps_offset:
                print("Aviso: Dados GPS não encontrados na imagem.")
                return None

            gps_data = tiff_header[gps_offset:]
            num_entradas_gps = struct.unpack(byte_order + 'H', gps_data[:2])[0]
            
            latitude = []
            longitude = []
            ref_latitude = ''
            ref_longitude = ''

            for i in range(num_entradas_gps):
                offset = 2 + i * 12
                tag_gps = struct.unpack(byte_order + 'H', gps_data[offset:offset+2])[0]
                tipo_gps = struct.unpack(byte_order + 'H', gps_data[offset+2:offset+4])[0]
                count_gps = struct.unpack(byte_order + 'I', gps_data[offset+4:offset+8])[0]
                valor_gps = gps_data[offset+8:offset+12]

                if tag_gps == 0x0001:
                    if tipo_gps == 2:
                        ref_latitude = valor_gps[:1].decode('ascii')
                elif tag_gps == 0x0002:
                    if tipo_gps == 5:
                        coord_offset = struct.unpack(byte_order + 'I', valor_gps)[0]
                        for j in range(3):
                            num = struct.unpack(byte_order + 'I', tiff_header[coord_offset+j*8:coord_offset+j*8+4])[0]
                            den = struct.unpack(byte_order + 'I', tiff_header[coord_offset+j*8+4:coord_offset+j*8+8])[0]
                            latitude.append(round(num/den, 6))
                elif tag_gps == 0x0003:
                    if tipo_gps == 2:
                        ref_longitude = valor_gps[:1].decode('ascii')
                elif tag_gps == 0x0004:
                    if tipo_gps == 5:
                        coord_offset = struct.unpack(byte_order + 'I', valor_gps)[0]
                        for j in range(3):
                            num = struct.unpack(byte_order + 'I', tiff_header[coord_offset+j*8:coord_offset+j*8+4])[0]
                            den = struct.unpack(byte_order + 'I', tiff_header[coord_offset+j*8+4:coord_offset+j*8+8])[0]
                            longitude.append(round(num/den, 6))

            if not latitude or not longitude:
                print("Aviso: Coordenadas GPS incompletas.")
                return None

            return {
                'latitude': latitude,
                'longitude': longitude,
                'ref_latitude': ref_latitude,
                'ref_longitude': ref_longitude
            }

    except Exception as e:
        print(f"Erro ao processar a imagem: {str(e)}")
        return None

def converter_para_decimal(graus, minutos, segundos, ref):
    decimal = graus + minutos/60 + segundos/3600
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def abrir_no_mapa(latitude, longitude, ref_lat, ref_lon):
    try:
        lat_decimal = converter_para_decimal(latitude[0], latitude[1], latitude[2], ref_lat)
        lon_decimal = converter_para_decimal(longitude[0], longitude[1], longitude[2], ref_lon)
        
        url = f"https://www.openstreetmap.org/?mlat={lat_decimal}&mlon={lon_decimal}&zoom=15"
        
        if sys.platform == 'win32':
            subprocess.Popen(['start', url], shell=True)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', url])
        else:
            subprocess.Popen(['xdg-open', url])
            
        return True
    except Exception as e:
        print(f"Erro ao abrir mapa: {str(e)}")
        return False

#Código principal executado diretamente
if len(sys.argv) < 2:
    print("Uso: python3 analise.py <arquivo_imagem>")
    sys.exit(1)
 
nome_arquivo = sys.argv[1]
if not os.path.exists(nome_arquivo):
    print(f"Erro: Arquivo não encontrado - {nome_arquivo}")
    sys.exit(1)

print(f"\nAnalisando imagem: {nome_arquivo}")

dados_gps = analisar_imagem(nome_arquivo)
if not dados_gps:
    print("Não foi possível extrair dados GPS da imagem.")
    sys.exit(1)

print("\nDados GPS encontrados:")
print(f"Latitude: {dados_gps['latitude']} {dados_gps['ref_latitude']}")
print(f"Longitude: {dados_gps['longitude']} {dados_gps['ref_longitude']}")

print("\nAbrindo no OpenStreetMap...")
if abrir_no_mapa(dados_gps['latitude'], dados_gps['longitude'], 
                 dados_gps['ref_latitude'], dados_gps['ref_longitude']):
    print("Mapa aberto com sucesso!")
else:
    print("Falha ao abrir o mapa.")