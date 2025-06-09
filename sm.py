#!/usr/bin/env python3

import random
from enum import Enum
from typing import List, Optional, Dict

class CardType(Enum):
    ENGINEER = "Engineer"
    TOOL = "Tool"
    SERVICE = "Service"
    INCIDENT = "Incident"
    PRACTICE = "Practice"
    ENVIRONMENT = "Environment"
    UPGRADE = "Upgrade"
    BANDWIDTH = "Bandwidth"

class Severity(Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"

class Vulnerability(Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"

class Card:
    def __init__(self, name: str, cost: int, card_type: CardType, description: str = ""):
        self.name = name
        self.cost = cost  # Bandwidth cost
        self.type = card_type
        self.description = description
        self.is_deployed = False

class Engineer(Card):
    def __init__(self, name: str, cost: int, health: int, morale_impact: int, 
                 ability: str = "", description: str = ""):
        super().__init__(name, cost, CardType.ENGINEER, description)
        self.health = health
        self.max_health = health
        self.morale_impact = morale_impact
        self.ability = ability
    
    def __str__(self):
        return f"{self.name} ({self.cost}B) - {self.health}HP, Morale: {self.morale_impact:+d}"

class Tool(Card):
    def __init__(self, name: str, cost: int, effect: str, description: str = ""):
        super().__init__(name, cost, CardType.TOOL, description)
        self.effect = effect
    
    def __str__(self):
        return f"{self.name} ({self.cost}B) - Tool: {self.effect}"

class Service(Card):
    def __init__(self, name: str, cost: int, health: int, uptime_yield: int, 
                 vulnerability: Vulnerability, description: str = ""):
        super().__init__(name, cost, CardType.SERVICE, description)
        self.health = health
        self.max_health = health
        self.uptime_yield = uptime_yield
        self.vulnerability = vulnerability
        self.turns_deployed = 0
    
    def __str__(self):
        return f"{self.name} ({self.cost}B) - {self.health}HP, +{self.uptime_yield}UP/3turns, Vuln: {self.vulnerability.value}"

class Incident(Card):
    def __init__(self, name: str, severity: Severity, effect: str, mitigation_cost: int = 0, description: str = ""):
        super().__init__(name, 0, CardType.INCIDENT, description)  # Incidents cost 0 to play
        self.severity = severity
        self.effect = effect
        self.mitigation_cost = mitigation_cost
    
    def __str__(self):
        return f"{self.name} - {self.severity.value} Incident: {self.effect}"

class Practice(Card):
    def __init__(self, name: str, cost: int, effect: str, description: str = ""):
        super().__init__(name, cost, CardType.PRACTICE, description)
        self.effect = effect
    
    def __str__(self):
        return f"{self.name} ({self.cost}B) - Practice: {self.effect}"

class Environment(Card):
    def __init__(self, name: str, cost: int, effect: str, description: str = ""):
        super().__init__(name, cost, CardType.ENVIRONMENT, description)
        self.effect = effect
    
    def __str__(self):
        return f"{self.name} ({self.cost}B) - Environment: {self.effect}"

class Upgrade(Card):
    def __init__(self, name: str, cost: int, effect: str, description: str = ""):
        super().__init__(name, cost, CardType.UPGRADE, description)
        self.effect = effect
    
    def __str__(self):
        return f"{self.name} ({self.cost}B) - Upgrade: {self.effect}"

class Bandwidth(Card):
    def __init__(self, name: str, bandwidth_value: int, description: str = ""):
        super().__init__(name, 0, CardType.BANDWIDTH, description)  # Bandwidth cards cost 0 to play
        self.bandwidth_value = bandwidth_value
    
    def __str__(self):
        return f"{self.name} - Provides {self.bandwidth_value} Bandwidth"

class Player:
    def __init__(self, name: str, deck: List[Card], is_human: bool = True):
        self.name = name
        self.deck = deck.copy()
        self.hand = []
        self.is_human = is_human  # True for human players, False for AI
        
        # Infrastructure state
        self.engineers = []  # Deployed engineers
        self.tools = []      # Deployed tools
        self.services = []   # Deployed services
        self.environment = None  # Current environment
        self.upgrades = []   # Deployed upgrades
        self.bandwidth_sources = []  # Deployed bandwidth cards
        
        # Resources
        self.bandwidth = 1  # Current available bandwidth
        self.max_bandwidth = 1  # Maximum bandwidth generation per turn
        self.uptime_points = 0
        self.service_health = 20  # Overall service health
        self.team_morale = 0
        self.security_posture = 50  # 0-100 scale
        self.tech_debt_tokens = 0
        self.blameless_culture = 50  # Hidden metric
        
        # Shuffle deck and draw starting hand
        random.shuffle(self.deck)
        self.draw_cards(5)
    
    def draw_cards(self, num: int = 1):
        """Draw cards from deck to hand"""
        for _ in range(num):
            if self.deck:
                self.hand.append(self.deck.pop())
    
    def calculate_total_morale(self) -> int:
        """Calculate total team morale from engineers"""
        return sum(engineer.morale_impact for engineer in self.engineers)
    
    def play_card(self, card_index: int) -> bool:
        """Play a card from hand"""
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            
            # Check bandwidth
            if card.cost <= self.bandwidth:
                self.bandwidth -= card.cost
                played_card = self.hand.pop(card_index)
                
                # Deploy based on card type
                if isinstance(played_card, Engineer):
                    self.engineers.append(played_card)
                    played_card.is_deployed = True
                    self.team_morale = self.calculate_total_morale()
                    print(f"{self.name} deployed {played_card.name}! Team morale now: {self.team_morale}")
                
                elif isinstance(played_card, Tool):
                    self.tools.append(played_card)
                    played_card.is_deployed = True
                    print(f"{self.name} deployed {played_card.name}!")
                
                elif isinstance(played_card, Service):
                    self.services.append(played_card)
                    played_card.is_deployed = True
                    print(f"{self.name} deployed {played_card.name}!")
                
                elif isinstance(played_card, Environment):
                    if self.environment:
                        print(f"Replacing {self.environment.name} with {played_card.name}")
                    self.environment = played_card
                    played_card.is_deployed = True
                    print(f"{self.name} set up {played_card.name} environment!")
                
                elif isinstance(played_card, Upgrade):
                    self.upgrades.append(played_card)
                    played_card.is_deployed = True
                    print(f"{self.name} implemented {played_card.name}!")
                
                elif isinstance(played_card, Bandwidth):
                    self.bandwidth_sources.append(played_card)
                    played_card.is_deployed = True
                    print(f"{self.name} deployed {played_card.name}! Will generate +{played_card.bandwidth_value} bandwidth each turn.")
                
                elif isinstance(played_card, Practice):
                    print(f"{self.name} executed {played_card.name}!")
                    # Practice effects are immediate
                
                return True
            else:
                print(f"Not enough bandwidth! Need {card.cost}, have {self.bandwidth}")
        return False
    
    def start_turn(self):
        """Actions at the start of each turn"""
        # Calculate max bandwidth from bandwidth cards
        base_bandwidth = 1  # Everyone starts with 1 base bandwidth
        bandwidth_from_cards = sum(card.bandwidth_value for card in self.bandwidth_sources)
        self.max_bandwidth = base_bandwidth + bandwidth_from_cards
        
        # Add new bandwidth to existing pool (like MTG lands)
        self.bandwidth += self.max_bandwidth
        
        # Environment effects (add to current bandwidth)
        if self.environment and "Public Cloud" in self.environment.name:
            self.bandwidth += 1  # Cloud gives extra bandwidth
            print(f"Public Cloud provides +1 bonus bandwidth!")
        
        # Service uptime generation
        for service in self.services:
            service.turns_deployed += 1
            if service.turns_deployed % 3 == 0:  # Every 3 turns
                self.uptime_points += service.uptime_yield
                print(f"{service.name} generated {service.uptime_yield} UP!")
        
        # Kubernetes auto-recovery
        for upgrade in self.upgrades:
            if "Kubernetes" in upgrade.name:
                for service in self.services:
                    if service.health < service.max_health:
                        service.health += 1
                        print(f"Kubernetes recovered 1 health for {service.name}")
        
        self.draw_cards(1)
        print(f"\n=== {self.name}'s Turn ===")
        print(f"Bandwidth: {self.bandwidth} (Generated {self.max_bandwidth} this turn)")
        print(f"Uptime Points: {self.uptime_points}/20")
        print(f"Service Health: {self.service_health}/20")
        print(f"Team Morale: {self.team_morale}")
    
    def show_hand(self):
        """Display player's hand"""
        print(f"\n{self.name}'s Hand:")
        for i, card in enumerate(self.hand):
            print(f"{i + 1}. {card}")
    
    def ai_play_turn(self):
        """AI decision making for computer players"""
        print(f"\n🤖 {self.name} (AI) is thinking...")
        
        # AI Strategy: Priority order
        # 1. Play bandwidth cards first (for economy)
        # 2. Play affordable engineers/services
        # 3. Play tools and upgrades
        # 4. Save bandwidth if nothing good available
        
        cards_played = 0
        max_cards_per_turn = 3  # Limit AI to prevent infinite loops
        
        while cards_played < max_cards_per_turn and self.bandwidth > 0:
            best_card_index = self.ai_choose_card()
            
            if best_card_index is not None:
                card = self.hand[best_card_index]
                print(f"🤖 {self.name} considers playing {card.name}...")
                
                if self.play_card(best_card_index):
                    cards_played += 1
                else:
                    break  # Something went wrong, stop trying
            else:
                break  # No good cards to play
        
        if cards_played == 0:
            print(f"🤖 {self.name} saves bandwidth for next turn.")
        
        print(f"🤖 {self.name} ends turn.")
    
    def show_infrastructure(self):
        """AI card selection logic"""
        affordable_cards = []
        
        # Find all affordable cards
        for i, card in enumerate(self.hand):
            if card.cost <= self.bandwidth:
                affordable_cards.append((i, card))
        
        if not affordable_cards:
            return None
        
        # AI Priority System
        priority_scores = []
        
        for index, card in affordable_cards:
            score = 0
            
            # Prioritize bandwidth cards (economy first)
            if isinstance(card, Bandwidth):
                score += 100  # Highest priority
                score += card.bandwidth_value * 10  # Prefer higher bandwidth
            
            # Engineers are important for board presence
            elif isinstance(card, Engineer):
                score += 80
                score += card.health * 5  # Prefer tanky engineers
                score += card.morale_impact * 3
            
            # Services generate uptime points
            elif isinstance(card, Service):
                score += 70
                score += card.uptime_yield * 10  # Prioritize high yield
                score += card.health * 3
            
            # Tools provide utility
            elif isinstance(card, Tool):
                score += 60
            
            # Upgrades are good long-term
            elif isinstance(card, Upgrade):
                score += 50
            
            # Environments can be situational
            elif isinstance(card, Environment):
                score += 40
                # Don't replace environment if we have one
                if self.environment:
                    score -= 30
            
            # Practices are immediate effect
            elif isinstance(card, Practice):
                score += 30
            
            # Prefer cheaper cards early game, expensive cards late game
            if len(self.bandwidth_sources) <= 2:  # Early game
                score += max(0, 10 - card.cost * 2)
            else:  # Late game
                score += card.cost
            
            priority_scores.append((index, score))
        
        # Choose highest scoring card
        if priority_scores:
            best_choice = max(priority_scores, key=lambda x: x[1])
            return best_choice[0]
        
        return None
        """Display deployed infrastructure"""
        print(f"\n{self.name}'s Infrastructure:")
        
        if self.engineers:
            print("Engineers:")
            for engineer in self.engineers:
                print(f"  - {engineer}")
        
        if self.services:
            print("Services:")
            for service in self.services:
                print(f"  - {service}")
        
        if self.tools:
            print("Tools:")
            for tool in self.tools:
                print(f"  - {tool}")
        
        if self.environment:
            print(f"Environment: {self.environment}")
        
        if self.upgrades:
            print("Upgrades:")
            for upgrade in self.upgrades:
                print(f"  - {upgrade}")
        
        if self.bandwidth_sources:
            print("Bandwidth Sources:")
            for bandwidth in self.bandwidth_sources:
                print(f"  - {bandwidth}")

class StackMastersGame:
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.current_player = 0
        self.turn_count = 1
        self.game_over = False
        self.winner = None
    
    def check_win_conditions(self):
        """Check if game is over"""
        for player in self.players:
            if player.uptime_points >= 20:
                self.winner = player
                self.game_over = True
                print(f"\n🎉 {player.name} wins with 20 Uptime Points!")
                return
            
            if player.service_health <= 0:
                self.winner = self.players[1 - self.players.index(player)]
                self.game_over = True
                print(f"\n💥 {self.winner.name} wins! {player.name}'s services crashed!")
                return
    
    def trigger_random_incident(self):
        """Randomly trigger incidents based on security posture"""
        current = self.players[self.current_player]
        
        # Higher security posture = lower incident chance
        incident_chance = max(10, 100 - current.security_posture)
        
        if random.randint(1, 100) <= incident_chance:
            incidents = [
                Incident("DDoS Attack", Severity.HIGH, "-3 Bandwidth next turn", 2),
                Incident("Memory Leak", Severity.MODERATE, "-2 Service Health", 1),
                Incident("SSL Certificate Expired", Severity.LOW, "-1 Uptime Point", 1),
                Incident("Database Corruption", Severity.CRITICAL, "-5 Service Health", 3),
            ]
            
            incident = random.choice(incidents)
            print(f"\n🚨 INCIDENT: {incident}")
            
            # Apply incident effects (simplified)
            if "Service Health" in incident.effect:
                damage = int(incident.effect.split('-')[1].split()[0])
                current.service_health -= damage
                print(f"{current.name} loses {damage} Service Health!")
    
    def next_turn(self):
        """Switch to next player's turn"""
        self.current_player = 1 - self.current_player
        if self.current_player == 0:
            self.turn_count += 1
        
        current = self.players[self.current_player]
        current.start_turn()
        
        # Random incidents
        self.trigger_random_incident()
        
        self.check_win_conditions()
    
    def play_interactive_turn(self):
        """Handle an interactive turn with player input"""
        if self.game_over:
            return
            
        current = self.players[self.current_player]
        
        # Check if current player is human or AI
        if not current.is_human:
            # AI turn
            print(f"\n{'='*50}")
            print(f"🤖 {current.name}'s turn (AI)")
            current.show_infrastructure()
            current.ai_play_turn()
            return
        
        # Human turn
        print(f"\n{'='*50}")
        current.show_hand()
        current.show_infrastructure()
        
        while True:
            print(f"\n{current.name}, what would you like to do?")
            print("1. Play a card from hand")
            print("2. View detailed infrastructure")
            print("3. View opponent's infrastructure") 
            print("4. End turn")
            print("5. View game status")
            
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == "1":
                    self.handle_play_card(current)
                elif choice == "2":
                    current.show_infrastructure()
                elif choice == "3":
                    opponent = self.players[1 - self.current_player]
                    print(f"\n{opponent.name}'s Infrastructure:")
                    opponent.show_infrastructure()
                elif choice == "4":
                    print(f"{current.name} ends their turn.")
                    break
                elif choice == "5":
                    self.show_game_status()
                else:
                    print("Invalid choice. Please enter 1-5.")
                    
            except KeyboardInterrupt:
                print("\nGame interrupted!")
                self.game_over = True
                return
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        self.check_win_conditions()
    
    def handle_play_card(self, player: Player):
        """Handle card playing with user input"""
        if not player.hand:
            print("No cards in hand!")
            return
            
        print(f"\nAvailable Bandwidth: {player.bandwidth} (Generates {player.max_bandwidth}/turn)")
        print("Select a card to play (or 0 to cancel):")
        
        # Show affordable cards
        affordable_cards = []
        for i, card in enumerate(player.hand):
            if card.cost <= player.bandwidth:
                affordable_cards.append(i)
                print(f"{i + 1}. ✅ {card}")
            else:
                print(f"{i + 1}. ❌ {card} (Need {card.cost - player.bandwidth} more bandwidth)")
        
        if not affordable_cards:
            print("No affordable cards!")
            return
            
        try:
            choice = int(input("\nEnter card number (0 to cancel): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(player.hand):
                card_index = choice - 1
                if card_index in affordable_cards:
                    success = player.play_card(card_index)
                    if success:
                        print(f"\n✅ Successfully played {player.hand[card_index].name}!" if card_index < len(player.hand) else "✅ Card played successfully!")
                    else:
                        print("❌ Failed to play card!")
                else:
                    print("❌ Cannot afford that card!")
            else:
                print("❌ Invalid card number!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def show_game_status(self):
        """Show current game status for both players"""
        print(f"\n{'='*60}")
        print(f"🎮 GAME STATUS - Turn {self.turn_count}")
        print(f"{'='*60}")
        
        for i, player in enumerate(self.players):
            status = "👑 CURRENT TURN" if i == self.current_player else ""
            print(f"\n🔹 {player.name} {status}")
            print(f"   💰 Uptime Points: {player.uptime_points}/20")
            print(f"   💚 Service Health: {player.service_health}/20")
            print(f"   ⚡ Bandwidth: {player.bandwidth} (Generates {player.max_bandwidth}/turn)")
            print(f"   😊 Team Morale: {player.team_morale}")
            print(f"   🛡️  Security Posture: {player.security_posture}")
            print(f"   📚 Cards in Hand: {len(player.hand)}")
            print(f"   👥 Engineers: {len(player.engineers)}")
            print(f"   🔧 Tools: {len(player.tools)}")
            print(f"   🖥️  Services: {len(player.services)}")
            print(f"   📡 Bandwidth Sources: {len(player.bandwidth_sources)}")
            
        print(f"\n{'='*60}")
    
    def setup_players(self):
        """Interactive player setup with human/AI selection"""
        print("🚀 Welcome to Stack Masters!")
        print("The DevOps/SRE Trading Card Game\n")
        
        print("Choose game mode:")
        print("1. Human vs Human")
        print("2. Human vs Computer")
        print("3. Computer vs Computer (watch AI battle!)")
        
        while True:
            try:
                mode = input("\nEnter your choice (1-3): ").strip()
                if mode in ["1", "2", "3"]:
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                exit()
        
        # Setup based on chosen mode
        if mode == "1":  # Human vs Human
            player1_name = input("Enter Player 1 name (or press Enter for 'Player 1'): ").strip()
            if not player1_name:
                player1_name = "Player 1"
            
            player2_name = input("Enter Player 2 name (or press Enter for 'Player 2'): ").strip()  
            if not player2_name:
                player2_name = "Player 2"
            
            self.players[0].name = player1_name
            self.players[0].is_human = True
            self.players[1].name = player2_name
            self.players[1].is_human = True
            
            print(f"\n🎯 {player1_name} vs {player2_name}")
            
        elif mode == "2":  # Human vs Computer
            player_name = input("Enter your name (or press Enter for 'Player'): ").strip()
            if not player_name:
                player_name = "Player"
            
            ai_names = ["CyberBot", "DevOps-AI", "SRE-9000", "CloudMind", "KubernetesBot", "MonitoringAI"]
            ai_name = random.choice(ai_names)
            
            # Randomly decide who goes first
            if random.choice([True, False]):
                self.players[0].name = player_name
                self.players[0].is_human = True
                self.players[1].name = ai_name
                self.players[1].is_human = False
                print(f"\n🎯 {player_name} (You) vs {ai_name} (AI)")
                print("You go first!")
            else:
                self.players[0].name = ai_name
                self.players[0].is_human = False
                self.players[1].name = player_name
                self.players[1].is_human = True
                print(f"\n🎯 {ai_name} (AI) vs {player_name} (You)")
                print("AI goes first!")
                
        else:  # Computer vs Computer
            ai_names = ["CyberBot", "DevOps-AI", "SRE-9000", "CloudMind", "KubernetesBot", "MonitoringAI", "SecurityBot", "DeploymentAI"]
            ai1_name = random.choice(ai_names)
            ai_names.remove(ai1_name)
            ai2_name = random.choice(ai_names)
            
            self.players[0].name = ai1_name
            self.players[0].is_human = False
            self.players[1].name = ai2_name
            self.players[1].is_human = False
            
            print(f"\n🤖 {ai1_name} vs {ai2_name}")
            print("Watch the AIs battle it out!")
        
        print("Goal: Reach 20 Uptime Points OR reduce opponent's Service Health to 0!")
        
        if mode == "3":  # AI vs AI
            input("\nPress Enter to start the AI battle...")
        else:
            input("\nPress Enter to start the game...")
    
    def play_full_game(self):
        """Play a complete interactive game"""
        self.setup_players()
        
        # Initial turn setup
        self.players[self.current_player].start_turn()
        
        while not self.game_over:
            current = self.players[self.current_player]
            
            self.play_interactive_turn()
            
            if not self.game_over:
                # Handle turn transitions differently for AI vs Human
                if current.is_human and not self.players[1 - self.current_player].is_human:
                    # Human to AI transition
                    input(f"\nPress Enter to let {self.players[1 - self.current_player].name} (AI) take their turn...")
                elif not current.is_human and self.players[1 - self.current_player].is_human:
                    # AI to Human transition  
                    input(f"\nPress Enter for your turn...")
                elif not current.is_human and not self.players[1 - self.current_player].is_human:
                    # AI to AI transition
                    input(f"\nPress Enter to continue to {self.players[1 - self.current_player].name}'s turn...")
                else:
                    # Human to Human transition
                    input(f"\nPress Enter to end {current.name}'s turn...")
                
                self.next_turn()
        
        # Game over
        if self.winner:
            print(f"\n🎉🏆 GAME OVER! 🏆🎉")
            winner_type = "🤖" if not self.winner.is_human else "👤"
            print(f"🎊 {winner_type} {self.winner.name} WINS! 🎊")
            
            # Final statistics
            print(f"\n📊 Final Statistics:")
            for player in self.players:
                player_type = "AI" if not player.is_human else "Human"
                print(f"\n{player.name} ({player_type}):")
                print(f"  Uptime Points: {player.uptime_points}")
                print(f"  Service Health: {player.service_health}")
                print(f"  Infrastructure: {len(player.engineers)} engineers, {len(player.services)} services")
        
        print(f"\nThanks for playing Stack Masters! 🚀")

# Sample deck creation for Stack Masters
def create_stack_masters_deck() -> List[Card]:
    """Create a sample Stack Masters deck"""
    deck = []
    
    # Engineers
    engineers = [
        Engineer("Junior Developer", 1, 2, 1, "Learns quickly"),
        Engineer("Senior SRE", 3, 3, 2, "Reduces incident damage by 1"),
        Engineer("Security Engineer", 2, 2, 1, "Improves security posture"),
        Engineer("DevOps Lead", 4, 4, 3, "Increases max bandwidth by 1"),
        Engineer("QA Engineer", 2, 2, 1, "Prevents some incidents"),
    ]
    
    for engineer in engineers:
        deck.extend([engineer] * 2)
    
    # Tools
    tools = [
        Tool("Prometheus", 2, "Monitoring - Reveal incidents early"),
        Tool("Jenkins", 1, "CI/CD - Deploy services faster"),
        Tool("Terraform", 2, "IaC - Consistent deployments"),
        Tool("Grafana", 1, "Dashboards - Better visibility"),
        Tool("Vault", 3, "Secrets - Improved security"),
    ]
    
    for tool in tools:
        deck.extend([tool] * 2)
    
    # Services
    services = [
        Service("Payment API", 2, 4, 3, Vulnerability.HIGH, "Critical payment processing"),
        Service("User Service", 1, 3, 2, Vulnerability.MODERATE, "User management"),
        Service("Analytics Engine", 3, 5, 2, Vulnerability.LOW, "Data processing"),
        Service("Notification Service", 1, 2, 1, Vulnerability.MODERATE, "Push notifications"),
    ]
    
    for service in services:
        deck.extend([service] * 2)
    
    # Practices
    practices = [
        Practice("Chaos Engineering", 1, "Test resilience - gain UP if services survive"),
        Practice("Postmortem", 1, "Learn from incidents - improve blameless culture"),
        Practice("Code Review", 1, "Reduce tech debt tokens"),
        Practice("Load Testing", 2, "Prevent performance incidents"),
    ]
    
    for practice in practices:
        deck.extend([practice] * 2)
    
    # Environments
    environments = [
        Environment("Public Cloud", 2, "+1 Bandwidth per turn, +1 Vulnerability"),
        Environment("On-Premises", 1, "Stable, less vulnerability"),
        Environment("Hybrid Cloud", 3, "Best of both worlds"),
    ]
    
    deck.extend(environments)
    
    # Upgrades
    upgrades = [
        Upgrade("Kubernetes", 3, "Auto-recover 1 Health per turn"),
        Upgrade("Serverless", 2, "Reduce service costs"),
        Upgrade("Containerization", 2, "Improve deployment speed"),
        Upgrade("Microservices", 4, "Isolate failures"),
    ]
    
    deck.extend(upgrades)
    
    # Bandwidth cards (essential for resource management)
    bandwidth_cards = [
        Bandwidth("Server Rack", 1, "Basic computing infrastructure"),
        Bandwidth("Network Switch", 1, "Network infrastructure"),
        Bandwidth("Load Balancer", 2, "High-capacity traffic management"),
        Bandwidth("CDN Node", 1, "Content delivery network"),
        Bandwidth("Database Cluster", 2, "Distributed data storage"),
        Bandwidth("Message Queue", 1, "Async communication infrastructure"),
        Bandwidth("Cache Layer", 1, "Performance optimization infrastructure"),
        Bandwidth("API Gateway", 1, "Service communication hub"),
    ]
    
    # Add multiple copies of bandwidth cards (they're essential!)
    for bandwidth in bandwidth_cards:
        if bandwidth.bandwidth_value == 1:
            deck.extend([bandwidth] * 4)  # 4 copies of 1-bandwidth cards
        else:
            deck.extend([bandwidth] * 2)  # 2 copies of 2-bandwidth cards
    
    return deck

# Example usage - Interactive Game with Player Type Selection
if __name__ == "__main__":
    # Create two players with Stack Masters decks
    deck1 = create_stack_masters_deck()
    deck2 = create_stack_masters_deck()
    
    player1 = Player("Player 1", deck1, is_human=True)  # Will be configured in setup
    player2 = Player("Player 2", deck2, is_human=True)  # Will be configured in setup
    
    # Start an interactive game
    game = StackMastersGame(player1, player2)
    
    # Play the full interactive game
    game.play_full_game()