import os
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

TOTAL_NUM_CAPTURES = 10
HALF_NUM_CAPTURES = TOTAL_NUM_CAPTURES // 2


def load_and_clean_csv(file_path):
    # Read the file and clean out non-numeric lines
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Filter out lines that do not contain numeric data
    cleaned_lines = []
    for line in lines:
        try:
            # Try converting each line to a list of floats
            cleaned_lines.append(
                list(map(float, line.strip().replace(";", "").split(",")))
            )
        except ValueError:
            # If conversion fails, skip the line
            continue

    # Convert the cleaned data into a NumPy array
    return np.array(cleaned_lines)


def stitch_matrices(matrices_row):
    """
    Stitch a list of matrices horizontally to form a single row.
    """
    return np.concatenate(matrices_row, axis=1)


def create_heatmap(data_matrix):
    # Create the heatmap
    heatmap = go.Figure(data=go.Heatmap(z=data_matrix))

    # Add layout settings with equal aspect ratio
    heatmap.update_layout(
        title="2D Heatmap of Combined Laser Profile Data",
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        xaxis=dict(
            range=[0, data_matrix.shape[1]],
            scaleanchor="y",  # Lock X-axis scale to Y-axis
            scaleratio=1      # 1:1 aspect ratio
        ),
        yaxis=dict(
            range=[0, data_matrix.shape[0]],
            scaleanchor="x",  # Lock Y-axis scale to X-axis
            scaleratio=1      # 1:1 aspect ratio
        ),
    )

    return heatmap


def main(directory_path):
    # Get list of all CSV files in the directory and sort them (if needed)
    csv_files = sorted([os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.csv')])

    # Split files into two groups for the bottom and top rows
    bottom_row_files = csv_files[:HALF_NUM_CAPTURES]
    top_row_files = csv_files[HALF_NUM_CAPTURES:TOTAL_NUM_CAPTURES]

    # Load and clean each CSV file, storing matrices in lists for each row
    bottom_row_matrices = [load_and_clean_csv(file) for file in bottom_row_files]
    top_row_matrices = [load_and_clean_csv(file) for file in top_row_files]

    # Stitch each row horizontally
    bottom_row = stitch_matrices(bottom_row_matrices)
    top_row = stitch_matrices(top_row_matrices)

    # Stitch the two rows vertically, with the top row above the bottom row
    stitched_matrix = np.concatenate([top_row, bottom_row], axis=0)

    # Generate the heatmap using the stitched data matrix
    heatmap = create_heatmap(stitched_matrix)

    # Save the heatmap as an HTML file
    pio.write_html(heatmap, file="combined_2d_heatmap.html", auto_open=True)


if __name__ == "__main__":
    # Replace this with the actual directory path containing your CSV files
    directory_path = "C:\\Users\\Finn\\Documents\\test64bit\\dataray_outputs"
    main(directory_path)
