#!/usr/bin/env python
"""
Gaussian Generation with FWHM - Standalone Module

This module provides functions to generate Gaussian curves with specified
Full Width Half Maximum (FWHM) and add them to existing arrays for visualization
and analysis.

Author: Generated for optical_seti project
Repository: https://github.com/spacetraveller42/optical_seti

Usage Example:
    import numpy as np
    import matplotlib.pyplot as plt
    from gaussian_generator import generate_gaussian, add_gaussian_to_array
    
    # Generate a Gaussian
    gaussian = generate_gaussian(fwhm=10.0, amplitude=100, center=50, array_length=100)
    
    # Add to existing data
    data = np.random.randn(100) * 5 + 500
    result = data + gaussian
    
    # Plot
    plt.plot(result)
    plt.show()
"""

import numpy as np
import matplotlib.pyplot as plt

FWHM_TO_SIGMA_FACTOR = 2 * np.sqrt(2 * np.log(2))

def generate_gaussian(fwhm, amplitude=None, center=None, array_length=None, area=None):
    if fwhm <= 0:
        raise ValueError(f"FWHM must be positive, got {fwhm}")
    if array_length <= 0:
        raise ValueError(f"array_length must be positive, got {array_length}")
    if center < 0 or center >= array_length:
        raise ValueError(f"center must be within [0, {array_length}), got {center}")
    
    if amplitude is None and area is None:
        raise ValueError("Either 'amplitude' or 'area' must be specified")
    if amplitude is not None and area is not None:
        raise ValueError("Cannot specify both 'amplitude' and 'area' - choose one")
    
    sigma = fwhm / FWHM_TO_SIGMA_FACTOR
    
    if area is not None:
        if area <= 0:
            raise ValueError(f"area must be positive, got {area}")
        amplitude = area / (sigma * np.sqrt(2 * np.pi))

    x = np.arange(array_length)
    gaussian_array = amplitude * np.exp(-((x - center) ** 2) / (2 * sigma ** 2))
    
    return gaussian_array


def add_gaussian_to_array(data, fwhm, amplitude=None, center=None, array_length=None, axis=-1, area=None):
    data = np.asarray(data)
    
    if data.size == 0:
        raise ValueError("Input data array is empty")
    
    if data.ndim > 1:
        if axis < 0:
            axis = data.ndim + axis
        
        if axis < 0 or axis >= data.ndim:
            raise ValueError(f"axis {axis} is out of bounds for array of dimension {data.ndim}")
        
        if array_length is None:
            array_length = data.shape[axis]
        
        if array_length <= 0:
            raise ValueError(f"array_length must be positive, got {array_length}")
        
        if center < 0 or center >= array_length:
            raise ValueError(f"center {center} is out of bounds for array_length {array_length}")
        
        gaussian = generate_gaussian(fwhm, amplitude=amplitude, center=center, array_length=array_length, area=area)
        
        data_len = data.shape[axis]
        gauss_len = len(gaussian)
        
        if gauss_len < data_len:
            pad_gaussian = np.zeros(data_len)
            pad_gaussian[:gauss_len] = gaussian
            gaussian = pad_gaussian
        elif gauss_len > data_len:
            gaussian = gaussian[:data_len]
        
        broadcast_shape = [1] * data.ndim
        broadcast_shape[axis] = len(gaussian)
        gaussian = gaussian.reshape(broadcast_shape)
        
        result = data + gaussian
    else:
        if array_length is None:
            array_length = len(data)
        
        if array_length <= 0:
            raise ValueError(f"array_length must be positive, got {array_length}")
        
        if center < 0 or center >= array_length:
            raise ValueError(f"center {center} is out of bounds for array_length {array_length}")
        
        gaussian = generate_gaussian(fwhm, amplitude=amplitude, center=center, array_length=array_length, area=area)
        
        data_len = len(data)
        gauss_len = len(gaussian)
        
        if gauss_len == data_len:
            result = data + gaussian
        elif gauss_len < data_len:
            padded_gaussian = np.zeros(data_len)
            padded_gaussian[:gauss_len] = gaussian
            result = data + padded_gaussian
        else:
            result = data + gaussian[:data_len]
    
    return result


def plot_gaussian_comparison(data, fwhm, amplitude, center, title="Gaussian Addition Comparison"):
    gaussian = generate_gaussian(fwhm, amplitude, center, len(data))
    result = data + gaussian
    
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    axes[0].plot(gaussian, 'b-', linewidth=2)
    axes[0].axhline(y=amplitude/2, color='r', linestyle='--', alpha=0.5, 
                    label=f'Half Max (FWHM={fwhm})')
    axes[0].axvline(x=center, color='g', linestyle=':', alpha=0.5, label='Center')
    axes[0].set_title(f'Gaussian (FWHM={fwhm}, Amplitude={amplitude})', 
                      fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Array Index')
    axes[0].set_ylabel('Value')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(data, 'gray', linewidth=1.5)
    axes[1].set_title('Original Data', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Array Index')
    axes[1].set_ylabel('Value')
    axes[1].grid(True, alpha=0.3)
    
    axes[2].plot(data, 'gray', alpha=0.4, linewidth=1, label='Original')
    axes[2].plot(result, 'b-', linewidth=2, label='With Gaussian')
    axes[2].axvline(x=center, color='r', linestyle=':', alpha=0.5)
    axes[2].set_title(title, fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Array Index')
    axes[2].set_ylabel('Value')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig, axes


def run_demo():
    print("=" * 70)
    print("GAUSSIAN GENERATION WITH FWHM - DEMONSTRATION")
    print("=" * 70)
    
    print("\n1. Generate a simple Gaussian:")
    fwhm = 15.0
    amplitude = 200.0
    center = 100.0
    array_length = 200
    
    gaussian = generate_gaussian(fwhm, amplitude, center, array_length)
    print(f"   ✓ Generated Gaussian with FWHM={fwhm}, amplitude={amplitude}")
    print(f"   ✓ Array shape: {gaussian.shape}")
    print(f"   ✓ Peak value: {np.max(gaussian):.2f}")
    print(f"   ✓ Peak location: {np.argmax(gaussian)}")
    
    print("\n2. Add Gaussian to existing spectral data:")
    spectral_data = np.random.randn(500) * 10 + 1000
    
    laser_signal = add_gaussian_to_array(
        spectral_data, 
        fwhm=5.0,
        amplitude=500,
        center=250
    )
    
    print(f"   ✓ Original data range: [{np.min(spectral_data):.2f}, {np.max(spectral_data):.2f}]")
    print(f"   ✓ With signal range: [{np.min(laser_signal):.2f}, {np.max(laser_signal):.2f}]")
    print(f"   ✓ Successfully added narrow Gaussian (FWHM=5.0)")
    
    print("\n3. Add multiple Gaussians with different FWHM values:")
    baseline = np.random.randn(1000) * 5 + 500
    
    result = add_gaussian_to_array(baseline, fwhm=4.0, amplitude=300, center=200)
    print(f"   ✓ Added narrow signal (FWHM=4.0) at pixel 200")
    
    result = add_gaussian_to_array(result, fwhm=12.0, amplitude=200, center=500)
    print(f"   ✓ Added medium signal (FWHM=12.0) at pixel 500")
    
    result = add_gaussian_to_array(result, fwhm=30.0, amplitude=150, center=800)
    print(f"   ✓ Added wide signal (FWHM=30.0) at pixel 800")
    
    print("\n4. Creating visualizations...")
    
    fig1, axes1 = plot_gaussian_comparison(
        spectral_data[:200], 
        fwhm=15.0, 
        amplitude=400.0, 
        center=100.0,
        title="Single Gaussian Addition"
    )
    plt.figure(fig1.number)
    plt.savefig('gaussian_demo_single.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved 'gaussian_demo_single.png'")
    
    fig2, axes2 = plt.subplots(figsize=(14, 6))
    axes2.plot(baseline, 'lightgray', alpha=0.5, linewidth=0.5, label='Baseline')
    axes2.plot(result, 'b-', linewidth=1.5, label='With 3 Gaussians')
    axes2.axvline(x=200, color='r', linestyle=':', alpha=0.5)
    axes2.axvline(x=500, color='r', linestyle=':', alpha=0.5)
    axes2.axvline(x=800, color='r', linestyle=':', alpha=0.5)
    axes2.set_title('Multiple Gaussians (FWHM: 4, 12, 30)', fontsize=14, fontweight='bold')
    axes2.set_xlabel('Pixel Index')
    axes2.set_ylabel('Flux')
    axes2.legend()
    axes2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('gaussian_demo_multiple.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved 'gaussian_demo_multiple.png'")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n✓ You CAN set the FWHM directly")
    print("✓ You GET a numpy array from generate_gaussian()")
    print("✓ You CAN add it directly to existing arrays")
    print("✓ Gaussians are clearly visible in plots")
    print("=" * 70)
    
    plt.show()


def run_tests():
    print("\n" + "=" * 70)
    print("RUNNING TESTS")
    print("=" * 70)
    
    all_passed = True
    
    print("\nTest 1: Basic Gaussian generation")
    try:
        gaussian = generate_gaussian(fwhm=10.0, amplitude=100.0, center=50.0, array_length=100)
        peak_index = np.argmax(gaussian)
        peak_value = np.max(gaussian)
        
        assert peak_index == 50, f"Peak at {peak_index}, expected 50"
        assert abs(peak_value - 100.0) < 0.01, f"Peak value {peak_value}, expected 100.0"
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        all_passed = False
    
    print("\nTest 2: Array addition")
    try:
        baseline = np.ones(100) * 50.0
        result = add_gaussian_to_array(baseline, fwhm=10.0, amplitude=100.0, center=50.0)
        expected_peak = 150.0
        actual_peak = np.max(result)
        
        assert abs(actual_peak - expected_peak) < 0.01, \
            f"Peak {actual_peak}, expected {expected_peak}"
        print("   ✓ PASSED")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        all_passed = False
    
    print("\nTest 3: Input validation")
    try:
        try:
            generate_gaussian(fwhm=-5.0, amplitude=100.0, center=50.0, array_length=100)
            print("   ✗ FAILED: Should have raised ValueError for negative FWHM")
            all_passed = False
        except ValueError:
            print("   ✓ Correctly rejected negative FWHM")
        
        try:
            generate_gaussian(fwhm=10.0, amplitude=100.0, center=150.0, array_length=100)
            print("   ✗ FAILED: Should have raised ValueError for out-of-bounds center")
            all_passed = False
        except ValueError:
            print("   ✓ Correctly rejected out-of-bounds center")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
        all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    import sys
    
    tests_passed = run_tests()
    
    if tests_passed:
        print("\n")
        run_demo()
    else:
        print("\nSkipping demo due to test failures.")
        sys.exit(1)
