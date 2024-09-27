# Evaluating Randomized Numbers for Cryptographic Purposes in the Quantum Era

## Introduction

In the rapidly evolving landscape of cryptography, ensuring the security of random number generation is paramount. With the advent of quantum computers, traditional random bit generators face new challenges. This work delves into the evaluation of various random bit generators, emphasizing their security and applicability in the age of quantum computing.

## Investigating Random Bit Generators

1. **Gap-Based Approach**: I propose a novel gap-based approach to assess the security strength of random bit generators. By analyzing the gaps between consecutive bits, insights are gained into their robustness against attacks.

2. **Quantum Random Bit Generators (QRBGs)**: Extending the investigation, QRBGs are explored. These generators leverage quantum phenomena, such as quantum noise or photon measurements, to produce truly random bits. The performance and suitability for cryptographic applications are evaluated.

## Understanding Existing Generators

Widely used random bit generators are examined, focusing on their construction, architecture, and properties. Key algorithms include:

1. **Pseudorandom Bit Generators (PRBGs)**: These algorithms generate sequences that appear random but are deterministic. The statistical properties and limitations are analyzed.

2. **True Random Number Generators (TRNGs)**: TRNGs exploit physical processes (e.g., electronic noise or radioactive decay) to produce genuinely random bits. The advantages and challenges are discussed.

## Designing an Advanced Random Bit Generator

The research informs the design of an advanced random bit generator (Synthetic_RBG). By combining insights from classical cryptographic PRBGs and quantum approaches, a robust, scalable and secure generator is aimed to meet cryptographic requirements. Which is desgned and developed for low latency environments and stand alone applicaitons.

## Assessing Randomness

1. **Gap-Based Analysis**: The proposed gap-based approach (**Gap Density Function**) is applied to evaluate the generated bit sequences. Graphical representations reveal patterns and highlight areas for improvement. The GDF test provides a comprehensive gap-based analysis of random sequences.

2. **NIST Statistical Test Suite**: The sequences are subjected to NIST's suite of statistical tests. These tests assess randomness, independence, and uniformity. By comparing results, a comprehensive view of each generator's performance is obtained.

## Conclusion

This work contributes to the field of cryptography by providing a thorough examination of random bit generators. Whether leveraging classical algorithms or exploring quantum possibilities, understanding randomness is crucial for secure communication and data protection.

#### Keywords: RBG algorithms, QRBG algorithms, NIST test suite
#### For more details, check the [RBG Algorithms by Chirag Patel](https://github.com/chiragpatel1229/Cryptographic-RBGs-Development-and-Analysis/tree/main/RBG_Algorithms_by_ChiragPatel) folder.

