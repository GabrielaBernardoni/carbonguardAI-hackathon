import pandas as pd
import random

def gerar_banco_dados():
    print("Gerando base de dados oficial...")
    
    dados = []
    
    # 1. CRIA O SERIAL DE SUCESSO (Para o Cenário Legítimo)
    dados.append({
        "serial_number": "AM-2024-8892", # Vamos usar esse no app
        "project_name": "Amazon Forest Keeper",
        "origin_state": "AM",
        "owner": "EcoCorp Global",
        "vintage": 2024,
        "status_registry": "Active", # ATIVO = BOM
        "available_balance": 50000,
        "last_audit": "2024-05-20"
    })
    
    # 2. CRIA O SERIAL DE FRAUDE DUPLA CONTAGEM (Para o Cenário Ruim)
    dados.append({
        "serial_number": "MT-2021-0045", # Vamos usar esse no app
        "project_name": "Soy & Forest Integration",
        "origin_state": "MT",
        "owner": "AgroX Business",
        "vintage": 2021,
        "status_registry": "Retired", # RETIRED = JÁ FOI USADO (FRAUDE TENTAR VENDER DE NOVO)
        "available_balance": 0,
        "last_audit": "2021-11-10"
    })

    # 3. Dados aleatórios 
    for i in range(100):
        dados.append({
            "serial_number": f"BR-{random.randint(2020,2024)}-{random.randint(1000,9999)}",
            "project_name": "Projeto Genérico Carbono",
            "origin_state": "SP",
            "owner": "Vendedor Aleatorio",
            "vintage": 2023,
            "status_registry": "Active",
            "available_balance": random.randint(100, 10000),
            "last_audit": "2023-01-01"
        })

    df = pd.DataFrame(dados)
    df.to_csv("carbon_registry.csv", index=False)
    print("✅ Arquivo carbon_registry.csv criado com os seriais corretos!")

if __name__ == "__main__":
    gerar_banco_dados()