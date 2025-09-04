import pandas as pd
from AnalyticsApp.models import Product


def load_data(file_path):
    """Load dataset from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_products_from_dataframe(dataframe):
    """Create Product instances from a DataFrame."""
    for _, row in dataframe.iterrows():
        Product.objects.create(
            name=row.get('name', ''),
            category=row['category'],
            price=row['price'],
            stock=row['stock']
            created_at=row['created_at']
        )


if __name__ == "__main__":
    data = load_data('large_dataset.csv')
    if data is not None:
        create_products_from_dataframe(data)

    

