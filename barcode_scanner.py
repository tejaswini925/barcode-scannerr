import cv2
from pyzbar.pyzbar import decode
import winsound  # For beep on Windows

# Product database
products = {
    "76222010501240": {"name": "mondelez" , "price": 10},
}

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Higher resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

detected_barcodes = set()  # To avoid duplicate detection

while True:
    ret, frame = cap.read()
    if not ret:
        break
    

    # Convert frame to grayscale for better detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.equalizeHist(gray)
    

    # Decode barcodes
    barcodes = decode(gray)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')

        if barcode_data not in detected_barcodes:
            detected_barcodes.add(barcode_data)
            print("Detected Barcode:", barcode_data)

            # Play beep
            winsound.Beep(1000, 200)  # 1000 Hz for 200 ms

            # Show product info
            if barcode_data in products:
                product = products[barcode_data]
                print(f"Product: {product['name']}, Price: ₹{product['price']}")
            else:
                print("Product not found!")

        # Draw rectangle and text on frame
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, barcode_data, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Barcode Scanner", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()