from tinySA import tinySA

class spectrumAnalyzer:
    def __init__(self):
        # spectrum analyzer
        self.analyzer = tinySA()

    def get_peak_frequency(self):
        peak_freq = self.analyzer.marker_value_freq()
        return peak_freq
    

# Main script for user interaction
if __name__ == "__main__":
    analyzer = spectrumAnalyzer()
    peak_freq = analyzer.get_peak_frequency()
    print(f"Peak Frequency: {peak_freq} Hz")
    