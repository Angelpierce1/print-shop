def calculate_pixels_for_list(sizes_list, dpi=300, bleed_inch=0.125):
    """
    Calculates minimum pixels for a specific list of print sizes.
    """
    print(f"{'SIZE (Inches)':<15} | {'MIN PIXELS (WxH)':<20} | {'MEGAPIXELS':<12}")
    print("-" * 55)
    
    for width, height in sizes_list:
        # Add bleed to total width/height (bleed is on both left/right and top/bottom)
        total_w_in = width + (bleed_inch * 2)
        total_h_in = height + (bleed_inch * 2)

        # Calculate pixels
        pixel_w = int(total_w_in * dpi)
        pixel_h = int(total_h_in * dpi)
        
        # Calculate Megapixels (MP)
        megapixels = round((pixel_w * pixel_h) / 1_000_000, 2)

        # Print formatted row
        size_lbl = f"{width}\" x {height}\""
        pixel_lbl = f"{pixel_w} x {pixel_h}"
        print(f"{size_lbl:<15} | {pixel_lbl:<20} | {megapixels} MP")

# --- YOUR SIZES ---
my_sizes = [
    (3, 5),
    (4, 6),
    (8, 10),
    (11, 17),
    (12, 18),
    (13, 19)
]

# Run calculation
if __name__ == "__main__":
    calculate_pixels_for_list(my_sizes)

