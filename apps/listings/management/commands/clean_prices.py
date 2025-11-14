from django.core.management.base import BaseCommand
from django.db import connection
from decimal import Decimal, InvalidOperation

class Command(BaseCommand):
    help = 'Finds and cleans invalid price data in Listing objects.'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Scanning for invalid price data...')
            
            # Directly query the database to fix price values
            cursor = connection.cursor()
            cursor.execute('SELECT id, price FROM listings_listing')
            rows = cursor.fetchall()
            
            if not rows:
                self.stdout.write(self.style.SUCCESS('No listings found.'))
                return
            
            self.stdout.write(f'Found {len(rows)} listings. Checking prices...')
            
            updates_to_make = []
            for listing_id, price in rows:
                try:
                    if price is None or price == '' or price == 0:
                        continue
                    
                    # Try to convert to string then Decimal
                    price_str = str(price)
                    Decimal(price_str)
                    
                    # If it's a very large integer (like 1200000 or 4567107893), 
                    # it might need to be treated as cents or needs division by 100
                    if isinstance(price, int) and price > 1000000:
                        # Assume these are in cents, convert to dollars
                        new_price = float(Decimal(str(price)) / 100)
                        updates_to_make.append((listing_id, new_price))
                        self.stdout.write(f'  Listing {listing_id}: {price} cents -> {new_price} dollars')
                
                except (InvalidOperation, ValueError) as e:
                    self.stdout.write(self.style.WARNING(f'  Listing {listing_id}: Invalid price {price}. Setting to 0.00'))
                    updates_to_make.append((listing_id, 0.00))
            
            # Execute all updates
            updated_count = 0
            for listing_id, new_price in updates_to_make:
                try:
                    cursor.execute(f'UPDATE listings_listing SET price = {new_price} WHERE id = {listing_id}')
                    updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to update listing {listing_id}: {e}'))
            
            connection.commit()
            self.stdout.write(self.style.SUCCESS(f'Successfully cleaned {updated_count} listings.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during price cleaning: {str(e)}'))
            import traceback
            traceback.print_exc()
