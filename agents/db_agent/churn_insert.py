import pandas as pd
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "zinkworks",
    "user": "postgres",
    "password": "postgres",
}


INSERT_QUERY = """
INSERT INTO customer_churn (
    customer_id,
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract,
    paperless_billing,
    payment_method,
    monthly_charges,
    total_charges,
    churn
)
VALUES (
    %(customer_id)s,
    %(gender)s,
    %(senior_citizen)s,
    %(partner)s,
    %(dependents)s,
    %(tenure)s,
    %(phone_service)s,
    %(multiple_lines)s,
    %(internet_service)s,
    %(online_security)s,
    %(online_backup)s,
    %(device_protection)s,
    %(tech_support)s,
    %(streaming_tv)s,
    %(streaming_movies)s,
    %(contract)s,
    %(paperless_billing)s,
    %(payment_method)s,
    %(monthly_charges)s,
    %(total_charges)s,
    %(churn)s
)
"""


def to_bool(value) -> bool:
    return str(value).strip().lower() == "yes"


def load_customer_data(excel_file_path: str) -> None:
    df = pd.read_excel(excel_file_path)

    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn:
            with conn.cursor() as cursor:
                for _, row in df.iterrows():
                    data = {
                        "customer_id": row["customerID"],
                        "gender": row["gender"],
                        "senior_citizen": bool(row["SeniorCitizen"]),
                        "partner": to_bool(row["Partner"]),
                        "dependents": to_bool(row["Dependents"]),
                        "tenure": int(row["tenure"]),
                        "phone_service": to_bool(row["PhoneService"]),
                        "multiple_lines": row["MultipleLines"],
                        "internet_service": row["InternetService"],
                        "online_security": row["OnlineSecurity"],
                        "online_backup": row["OnlineBackup"],
                        "device_protection": row["DeviceProtection"],
                        "tech_support": row["TechSupport"],
                        "streaming_tv": row["StreamingTV"],
                        "streaming_movies": row["StreamingMovies"],
                        "contract": row["Contract"],
                        "paperless_billing": to_bool(row["PaperlessBilling"]),
                        "payment_method": row["PaymentMethod"],
                        "monthly_charges": float(row["MonthlyCharges"]),
                        "total_charges": float(
                            row["TotalCharges"]
                            if isinstance(row["TotalCharges"], float)
                            else 0
                        ),
                        "churn": to_bool(row["Churn"]),
                    }

                    cursor.execute(INSERT_QUERY, data)

        print("Customer data inserted successfully.")

    finally:
        conn.close()


if __name__ == "__main__":
    load_customer_data("Telecom.xlsx")
