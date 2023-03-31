import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Absorption Graph")
    st.title("Absorption Graph")

    # File upload
    st.sidebar.title("Upload data")
    file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])
    if file is None:
        st.sidebar.info("Please upload a file.")
        return

    # Load data
    if file.name.endswith(".csv"):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    # Get user input
    st.sidebar.title("Settings")
    min_wavelength = st.sidebar.number_input("Enter the minimum wavelength (in nm)", value=200)
    max_wavelength = st.sidebar.number_input("Enter the maximum wavelength (in nm)", value=600)
    min_absorption = st.sidebar.number_input("Enter the minimum absorption", value=0.0)
    max_absorption = st.sidebar.number_input("Enter the maximum absorption", value=2.0)

    # Filter data
    theoretical_data = data.iloc[:, :2]
    experimental_data = data.iloc[:, 2:]
    theoretical_data = theoretical_data[(theoretical_data.iloc[:, 0] >= min_wavelength) & (theoretical_data.iloc[:, 0] <= max_wavelength)]
    experimental_data = experimental_data[(experimental_data.iloc[:, 0] >= min_wavelength) & (experimental_data.iloc[:, 0] <= max_wavelength)]
    theoretical_data = theoretical_data[(theoretical_data.iloc[:, 1] >= min_absorption) & (theoretical_data.iloc[:, 1] <= max_absorption)]
    experimental_data = experimental_data[(experimental_data.iloc[:, 1] >= min_absorption) & (experimental_data.iloc[:, 1] <= max_absorption)]
    theoretical_data.iloc[:, 1] /= theoretical_data.iloc[:, 1].max()
    experimental_data.iloc[:, 1] /= experimental_data.iloc[:, 1].max()
    
     # Add labels and legend
    fig, ax = plt.subplots()
    default_x_title = "Wavelength (nm)"
    x_axis_title = st.text_input("Enter the title for the x-axis or press Enter to use default:", default_x_title)

    default_y_title = "Absorption"
    y_axis_title = st.text_input("Enter the title for the y-axis or press Enter to use default:", default_y_title)

    ax.set_xlabel(x_axis_title, fontsize=14)
    ax.set_ylabel(y_axis_title, fontsize=14)
    ax.legend(fontsize=12, loc='best', borderpad=1, borderaxespad=1, frameon=True, edgecolor='black', fancybox=True, shadow=True)

        # Define the default background color for the plot
    DEFAULT_BG_COLOR = "#FFF1D7"

    # Create a color picker widget to allow the user to select a background color
    bg_color = st.color_picker("Select a background color", DEFAULT_BG_COLOR)

    # Create a figure and axis object for the plot
    #fig, ax = plt.subplots()

    # Set the background color of the axis to the user-selected color
    ax.set_facecolor(bg_color)

    # Plot data
    ax.scatter(theoretical_data.iloc[:, 0], theoretical_data.iloc[:, 1], c='red', label="Experimental", marker='o', s=20)
    ax.scatter(experimental_data.iloc[:, 0], experimental_data.iloc[:, 1], c='green', label="Theoretical", marker='o', s=20)
    ax.set_xlabel("Wavelength (nm)", fontsize=14)
    ax.set_ylabel("Absorption", fontsize=14)
    ax.legend(fontsize=12)
    ax.set_title("Absorption Spectra of the Investigated Complexes", fontsize=16, fontweight='bold')
    ax.grid(alpha=0.3, color='gray')

    # Add watermark
    watermark_text = "Snehasis Banerjee"
    fig.text(0.5, 0.5, watermark_text, ha='center', va='center', fontsize=36, color='gray', alpha=0.3)

    # Save the plot as a high-resolution image
    output_file = file.name.split('.')[0] + '.jpg'
    plt.savefig(output_file, dpi=1200, bbox_inches='tight')

    # Show plot
    st.pyplot(fig)
if __name__ == "__main__":
    main()
