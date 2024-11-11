def calculate_1rm(weight, reps):
    """Estimate the one-rep max (1RM) based on weight and reps."""
    if reps == 1:
        return weight
    return weight * (1 + 0.0333 * reps)

def calculate_percentages(one_rm):
    """Calculate different percentages of the 1RM."""
    percentages = [0.20, 0.30, 0.40, 0.50, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    results = {f"{int(p*100)}%": round(one_rm * p, 2) for p in percentages}
    return results

# def main():
#     """Main function to run the calculator."""
#     print("Welcome to the 1RM Calculator!")
    
#     weight = float(input("Enter the weight lifted (in lbs): "))
#     reps = int(input("Enter the number of reps performed: "))
    
#     one_rm = calculate_1rm(weight, reps)
#     print(f"Estimated 1RM: {one_rm:.2f} lbs")
    
#     percentages = calculate_percentages(one_rm)
#     print("\nPercentages of 1RM:")
#     for percent, weight in percentages.items():
#         print(f"{percent}: {weight:.2f} lbs")

# if __name__ == "__main__":
#     main()
