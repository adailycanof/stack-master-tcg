# The DevOps/SRE/DevSecOps Trading Card Game - Stack Masters

![Stack Masters Logo](/stack-masters.png)

### 🎯 **OBJECTIVE**
Build and maintain the most reliable, secure, and efficient infrastructure. Win by either:
- Reaching **20 Uptime Points (UP)** first, OR
- Reducing your opponent's **Service Health** to zero



## 🚀 **HOW TO RUN THIS GAME**

### **System Requirements**
- **Python 3.6 or higher** (check with `python --version` or `python3 --version`)
- **Operating System:** Windows, macOS, or Linux
- **Terminal/Command Prompt** access
- **No additional libraries required** - uses only Python built-ins

### **Installation & Setup**

#### **Step 1: Get the Game Files**
1. Save the Python code as `stack_masters.py` (or `sm.py`)
2. Make sure the file is in a directory you can access from terminal

#### **Step 2: Run the Game**

**Option A: Using Python Command**
```bash
python stack_masters.py
```
or
```bash
python3 stack_masters.py
```

**Option B: Make it Executable (Linux/macOS)**
```bash
chmod +x stack_masters.py
./stack_masters.py
```

#### **Step 3: Choose Your Game Mode**
When you run the game, you'll see:
```
🚀 Welcome to Stack Masters!
The DevOps/SRE Trading Card Game

Choose game mode:
1. Human vs Human
2. Human vs Computer  
3. Computer vs Computer (watch AI battle!)

Enter your choice (1-3):
```
---
## Stack Masters - Official Rules

## 🃏 **CARD TYPES**

### 👨‍💼 **Engineers**
- **Purpose:** Your team members who build and maintain infrastructure
- **Stats:** Bandwidth Cost, Health, Morale Impact, Special Abilities
- **Examples:** Junior Developer, Senior SRE, Security Engineer, DevOps Lead
- **Notes:** Engineers provide ongoing effects and can be targeted by incidents

### 📡 **Bandwidth Cards**
- **Purpose:** Provide the bandwidth (resources) needed to play other cards
- **Cost:** Always 0 bandwidth to play
- **Effect:** Permanently increase your bandwidth generation each turn
- **Examples:** Server Rack (+1), Load Balancer (+2), Database Cluster (+2)
- **Strategy:** Essential for economy - play these early and often

### 🔧 **Tools**
- **Purpose:** Provide ongoing utility and automation
- **Examples:** Prometheus (monitoring), Jenkins (CI/CD), Terraform (IaC)
- **Effect:** Persistent benefits while deployed

### 🖥️ **Services**
- **Purpose:** Generate Uptime Points and represent your live applications
- **Stats:** Bandwidth Cost, Health, Uptime Yield, Vulnerability Level
- **Uptime Generation:** Generate UP every 3 turns based on their yield
- **Vulnerability:** Determines susceptibility to incidents (Low/Moderate/High)

### ⚡ **Incidents**
- **Purpose:** Represent failures, attacks, and problems
- **Cost:** 0 bandwidth (triggered automatically or by opponent)
- **Stats:** Severity level, Effect, Mitigation Cost
- **Examples:** DDoS Attack, Memory Leak, SSL Certificate Expired

### 🏢 **Environments**
- **Purpose:** Set your infrastructure context
- **Effect:** Global effects on your entire infrastructure
- **Limit:** Only one Environment can be active at a time
- **Examples:** Public Cloud (+1 bandwidth, +1 vulnerability), On-Premises (stable)

### ⚖️ **Practices**
- **Purpose:** Immediate-effect cards representing methodologies
- **Examples:** Chaos Engineering, Postmortems, Code Reviews
- **Effect:** One-time benefits when played

### ⬆️ **Upgrades**
- **Purpose:** Permanent infrastructure improvements
- **Examples:** Kubernetes (auto-heal), Serverless (reduce costs), Microservices
- **Effect:** Ongoing benefits for the rest of the game

---

## 🎮 **GAME SETUP**

### **Deck Construction**
- **Minimum 40 cards** (recommended mix includes bandwidth cards)
- **Suggested ratio:** 30% Bandwidth, 25% Engineers/Services, 45% Tools/Upgrades/Practices

### **Starting Conditions**
- Each player starts with **5 cards** in hand
- **20 Service Health**
- **0 Uptime Points**
- **1 base bandwidth** per turn
- Shuffle your deck and place it face-down

---

## 🔄 **TURN STRUCTURE**

### **Phase 1: Start of Turn**
1. **Generate Bandwidth:** Add your bandwidth generation to existing pool
   - Base: 1 bandwidth per turn
   - Plus: +1 for each deployed Bandwidth card
   - Plus: Environment bonuses (if any)
2. **Draw 1 Card** from your deck
3. **Service Uptime:** Services generate UP every 3rd turn deployed
4. **Automatic Effects:** Kubernetes healing, tool effects, etc.

### **Phase 2: Main Phase**
- **Play Cards:** Spend bandwidth to deploy cards from your hand
- **Multiple Cards:** Can play multiple cards if you have bandwidth
- **Free Cards:** Bandwidth cards always cost 0
- **Saving Bandwidth:** Unused bandwidth carries over to next turn

### **Phase 3: End Turn**
- **Declare End:** Pass turn to opponent
- **Hand Limit:** No maximum hand size
- **Incident Check:** Random incidents may trigger based on Security Posture

---

## 💰 **BANDWIDTH SYSTEM**

### **Key Mechanics**
- **Accumulation:** Unused bandwidth carries over (like MTG mana)
- **Generation:** Each turn adds new bandwidth to your existing pool
- **Strategy:** Save up for expensive cards or spend immediately

### **Example Bandwidth Flow**
```
Turn 1: 1 bandwidth → Play Server Rack (free) → End with 1 bandwidth
Turn 2: 1 + 2 = 3 bandwidth → Play Junior Dev (1 cost) → End with 2 bandwidth
Turn 3: 2 + 2 = 4 bandwidth → Save up → End with 4 bandwidth
Turn 4: 4 + 2 = 6 bandwidth → Play expensive card → Continue...
```

---

## 🏆 **WIN CONDITIONS**

### **Victory Method 1: Uptime Points**
- **Target:** First player to reach 20 UP wins
- **Generation:** Services generate UP every 3 turns
- **Bonus Sources:** Some Practices and special effects

### **Victory Method 2: Service Health**
- **Target:** Reduce opponent's Service Health to 0
- **Damage Sources:** Incidents, attacks, system failures
- **Defense:** Engineers, tools, and practices can mitigate damage

---

## 🚨 **INCIDENT SYSTEM**

### **Incident Triggers**
- **Random Events:** Based on Security Posture (lower = more incidents)
- **Opponent Cards:** Some cards may trigger incidents
- **Automatic:** Certain game states may cause incidents

### **Incident Resolution**
- **Immediate Effect:** Damage occurs when incident triggers
- **Mitigation:** Can be reduced by Engineers, Tools, or spending bandwidth
- **Severity Levels:** Low, Moderate, High, Critical

---

## 🛡️ **ADVANCED MECHANICS**

### **Team Morale**
- **Calculation:** Sum of all Engineers' Morale Impact
- **Effects:** Positive morale provides various bonuses
- **Affected By:** Incidents can reduce morale

### **Security Posture**
- **Scale:** 0-100 (50 is starting value)
- **Effects:** Higher security = fewer random incidents
- **Improved By:** Security Engineers, security tools

### **Tech Debt Tokens**
- **Accumulation:** Gained by rushing deployment or skipping practices
- **Consequences:** May trigger failures or reduce efficiency
- **Mitigation:** Code Reviews and other practices can reduce tech debt

### **Blameless Culture Meter**
- **Hidden Metric:** Tracks team culture health
- **Effects:** High blameless culture reduces incident severity
- **Improved By:** Postmortems, good management practices

---

## 📋 **CARD INTERACTION RULES**

### **Deployment Rules**
- **Bandwidth Cards:** Can always be played (cost 0)
- **Multiple Engineers:** Can have multiple Engineers of same type
- **Single Environment:** Only one Environment active at a time
- **Tool Stacking:** Multiple tools can be active simultaneously

### **Timing Rules**
- **Immediate Effects:** Practices and some tools activate immediately
- **Persistent Effects:** Engineers, Services, Tools remain until destroyed
- **Turn-Based Effects:** Service uptime, bandwidth generation occur each turn

### **Destruction Rules**
- **Engineer Health:** Engineers can be damaged by incidents
- **Service Health:** Services can be damaged, affecting uptime generation
- **Permanent Destruction:** Cards with 0 health are removed from play

---

## 🎯 **STRATEGY TIPS**

### **Early Game (Turns 1-3)**
- **Priority:** Deploy Bandwidth cards for economy
- **Foundation:** Get 3-4 bandwidth sources quickly
- **Defense:** Consider basic monitoring tools

### **Mid Game (Turns 4-7)**
- **Development:** Deploy Engineers and Services
- **Balance:** Mix offense (services) with defense (tools)
- **Efficiency:** Use accumulated bandwidth for power plays

### **Late Game (Turns 8+)**
- **Power Plays:** Deploy expensive, game-changing cards
- **Protection:** Maintain security and incident response
- **Victory Push:** Focus on win conditions

### **Universal Tips**
- **Economy First:** Bandwidth cards are crucial - don't neglect them
- **Diversify:** Don't put all resources into one strategy
- **Defend:** Monitor your Service Health and Security Posture
- **Adapt:** Respond to opponent's strategy and random incidents

---

## 🎮 **MULTIPLAYER VARIANTS**

### **2-Player Standard**
- Standard rules as described above
- Best experience for competitive play

### **3-4 Player Chaos**
- **Modified Win Conditions:** First to 25 UP or last player standing
- **Incident Spread:** Incidents can affect multiple players
- **Alliance Rules:** Temporary cooperation allowed but not binding

### **Solo Practice**
- **vs AI:** Practice against computer opponents
- **Difficulty Levels:** Adjust AI intelligence and starting advantages
- **Learning Mode:** Tutorial scenarios for new players

---

## 📖 **QUICK REFERENCE**

### **Turn Sequence**
1. Generate bandwidth → 2. Draw card → 3. Play cards → 4. End turn

### **Win Conditions**
- 20 Uptime Points OR opponent's Service Health = 0

### **Key Numbers**
- Starting Service Health: 20
- Starting hand size: 5
- Base bandwidth per turn: 1
- Service uptime frequency: Every 3 turns

### **Card Costs**
- Bandwidth cards: Always 0
- Engineers: 1-4 bandwidth
- Services: 1-3 bandwidth  
- Tools: 1-3 bandwidth
- Upgrades: 2-4 bandwidth

---

*Stack Masters - Where Infrastructure Meets Strategy* 🚀


## WIP ##