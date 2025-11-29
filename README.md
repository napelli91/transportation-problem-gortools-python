# 🚚 Transportation Problem with Google OR-Tools

A Linear Programming Approach

This repository implements and experiments with a **Transportation Problem** using **Google OR-Tools**.
The goal is to determine the optimal shipment plan from multiple warehouses to multiple retail stores,
minimizing total transportation cost while satisfying all stock and demand constraints.

## 📘 Problem Description

We consider a company with:

- **D** warehouses (depots), indexed by $d$
- **L** retail stores (locals), indexed by $l$
- **N** types of products, indexed by $n$

For each product, we know:

- The **available stock** at each warehouse
- The **demand** at each retail store
- The **unit transportation cost** for sending one unit of each product from each warehouse to each store

The objective is to compute the **optimal transportation plan**—that is, how many units of each
product should be transported from each warehouse to each store—such that:

- Total transportation cost is **minimized**
- Warehouse stock limits are respected$
- Store demand is fully satisfied$

This problem is related to the **Assignment Problem**, which has specific polynomial-time
algorithms (e.g., the Hungarian Algorithm). However, Linear Programming is more flexible and
accommodates multiple products, capacities, and more complex business constraints—hence
its relevance here.

## 🧮 Mathematical Model

### **Indices**

- $d$: Warehouse index$
- $l$: Store index$
- $n$: Product index$

### **Constants**

- $D$: Total number of warehouses$
- $L$: Total number of stores$
- $N$: Total number of products$
- $S_d^n$: Stock of product $n$ at warehouse $d$
- $T_l^n$: Demand of product $n$ at store $l$

### **Variables**

- $c_{dl}^n$: Cost of shipping one unit of product $n$ from warehouse $d$ to store $l$
- $x_{dl}^n$: Number of units of product $n$ shipped from warehouse $d$ to store $l$
- Integer and non-negative

## 🎯 Objective Function

Minimize total transportation costs:

$$
  \min \left(
  \sum_{n=1}^{N} \sum_{d=1}^{D} \sum_{l=1}^{L} c_{dl}^n \, x_{dl}^n
  \right)
$$

## 📏 Constraints

### **1. Non-negativity**

$$
x_{dl}^n \ge 0 \quad \forall d,l,n
$$

### **2. Warehouse supply limit**

$$
\sum_{l=1}^{L} x_{dl}^n \le S_d^n \quad \forall d,n
$$

### **3. Store demand cannot be exceeded**

$$
\sum_{d=1}^{D} x_{dl}^n \le T_l^n \quad \forall l,n
$$

### **4. Store demand must be satisfied**

$$
\sum_{d=1}^{D} x_{dl}^n \ge T_l^n \quad \forall l,n
$$

## 🔍 Understanding the Constraints

1. Non-negativity
  This condition states that all shipment quantities must be greater than
  or equal to zero. In practical terms, it simply means:
    - You **cannot ship a negative number of units** of a product.
    - Every decision variable $x_{dl}^n$ represents a real, physical shipment, so it must be zero or positive.
  Without this constraint, the solver could try to "cheat" by using
  negative values to artificially reduce the total cost.

2. Warehouse supply limit
  This constraint ensures that the **total quantity shipped out of a warehouse**
  for a given product does not exceed the stock available at that warehouse:
    - For each warehouse $d$ and product $n$, we sum all shipments from warehouse $d$ to every store $l$.
    - That sum cannot be greater than the stock $S_d^n$.
  Intuitively:
    - You **cannot ship more units of a product than you physically have** in that warehouse.
    - This models the **capacity / availability** of each warehouse for each product.

3. Store demand cannot be exceeded
  This constraint limits the **total quantity received by a store** for a
  given product so that it does not exceed its demand:
    - For each store $l$ and product $n$, we sum all shipments coming from every warehouse $d$.
    - That sum cannot be greater than the demand $T_l^n$.
  This reflects situations where:
    - A store has a **maximum demand or capacity** for a product.
    - Sending more units than this would either be wasteful or infeasible (e.g., storage limits).

4. Store demand must be satisfied
  This condition enforces that **each store actually receives enough units** of
  each product to cover its demand:
    - For each store $l$ and product $n$, the total incoming shipments from all warehouses must be at least $T_l^n$.
  Taken together with constraint 3 ("cannot be exceeded"), this means:
    - The total received must be **exactly equal** to the demand $T_l^n$ for each store and product.
    - In other words, every store gets **precisely what it needs**, no more and no less.
  These constraints as a whole guarantee that the solution is both
  **feasible in the real world** (no negative shipments, no exceeding stock,
  no oversupplying stores) and **aligned with business goals**
  (all customer demand is met).

## 🛠️ Implementation (Python + OR-Tools)

The model is implemented using the **Google OR-Tools Linear Solver**.

Example structure:

```sh
/project-root
 ├── input_data/
 ├── output_data/
 ├── src/
 │    ├── utils.py
 │    └── transportation_problem_solver.py
 ├── experimentation.py
 └── README.md
```

> You can run experiments varying the number of warehouses, stores, and products to evaluate performance.

## 📊 Experiments

You are encouraged to:

- Generate different problem instances
- Vary the number of warehouses and stores
- Measure execution time
- Compare results with heuristic or assignment-based approaches$

## 🤝 Contributing

Pull requests are welcome! If you'd like to extend the model, experiment
further, or optimize performance, feel free to contribute.

## 📄 License

This project is released under the MIT License.
