def two_sum(nums, target):
    num_to_index = {} # Created a dictionary to store the values and its index

    # We use a for loop to iterate through numbs list
    # The enumarate function provides both the index (i) and the value (num) of each element 
    for i, num in enumerate(nums):

        # We substract the num from target
        complement = target - num

        if complement in num_to_index:

            return [num_to_index[complement], i]
    
        num_to_index[num] = i

    return []

# Array called nums
nums = [2, 7, 11, 15]

# The target value, the goal is to find two indcies such that the number at those indixies 
# add up to the target.
target = 9

print(two_sum(nums, target))
    

def two_sum(transactions, target_id):
    id_to_index = {}
    
    for i, (transaction_id, _) in enumerate(transactions):
        if transaction_id == target_id:
            return [id_to_index.get(target_id), i]
        
        id_to_index[transaction_id] = i
    
    return []

# Example usage
def detect_duplicate_transactions(transactions):
    # Example: Detect pairs of transactions with the same ID
    target_id = 123456789  # Example transaction ID to check
    result_indices = two_sum(transactions, target_id)
    
    if result_indices:
        print(f"Duplicate transactions detected! Transactions {result_indices} have matching IDs.")
    else:
        print("No duplicate transactions detected.")

# Sample transaction data (ID, Amount)
transactions = [
    (123456789, 100.0),
    (234567890, 200.0),
    (123456789, 300.0),  # Duplicate ID
    (345678901, 400.0)
]

detect_duplicate_transactions(transactions)

def length_of_longest_substring(s):
    char_index_map = {}
    left = 0
    result = 0
    
    for right in range(len(s)):
        if s[right] in char_index_map:
            left = max(left, char_index_map[s[right]] + 1)
        
        result = max(result, right - left + 1)
        char_index_map[s[right]] = right
    
    return result

# Example usage
def ensure_unique_customer_id(customer_ids):
    longest_substring_length = length_of_longest_substring(customer_ids)
    print(f"Length of the longest substring without repeating characters: {longest_substring_length}")
    
    if longest_substring_length < 10:  # Example threshold
        print("Customer ID is too short. Consider generating a longer one.")
    else:
        print("Customer ID is valid.")

# Sample customer IDs
customer_ids = "CUST123456789"
ensure_unique_customer_id(customer_ids)

def two_sum(transactions, target_amount):
    amount_to_index = {}
    
    for i, (transaction_id, amount) in enumerate(transactions):
        if amount == target_amount:
            return [amount_to_index.get(target_amount), i]
        
        amount_to_index[amount] = i
    
    return []

# Example usage
def detect_anomalies(transactions, threshold):
    # Detect pairs of transactions with similar amounts (potential anomalies)
    for amount in set([t[1] for t in transactions]):
        if abs(amount - threshold) < 0.1:  # Example threshold
            result_indices = two_sum(transactions, amount)
            if result_indices:
                print(f"Anomaly detected! Transactions {result_indices} have similar amounts.")
    
    print("No anomalies detected.")

# Sample transaction data (ID, Amount)
transactions = [
    (123456789, 100.0),
    (234567890, 200.0),
    (123456789, 300.0),  # Duplicate ID
    (345678901, 400.0)
]

detect_anomalies(transactions, 350.0)  # Example threshold amount
