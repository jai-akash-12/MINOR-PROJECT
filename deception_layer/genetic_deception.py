"""
GENETIC ALGORITHM DECEPTION EVOLUTION - CORE INNOVATION
Uses GA to evolve the most effective deception strategies

This is a novel application of GA to cybersecurity defense (not malware)
RESEARCH CONTRIBUTION: First implementation of GA for deception optimization
"""

import random
import numpy as np
import copy
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utilities.config import GA_CONFIG
from utilities.logger import get_logger, DeceptionLogger
from utilities.metrics import global_metrics

logger = get_logger('genetic_algorithm')
deception_logger = DeceptionLogger()


class GeneticDeceptionEvolver:
    """
    Evolves deception strategies using Genetic Algorithms
    
    RESEARCH NOVELTY: GA optimizes deception effectiveness, not detection
    Fitness = Attacker engagement + Data collected + Confusion metrics
    """
    
    def __init__(self):
        self.population_size = GA_CONFIG['population_size']
        self.mutation_rate = GA_CONFIG['mutation_rate']
        self.crossover_rate = GA_CONFIG['crossover_rate']
        self.elite_size = GA_CONFIG['elite_size']
        self.fitness_weights = GA_CONFIG['fitness_weights']
        
        self.population = []
        self.generation = 0
        self.fitness_history = []
        self.best_chromosome_history = []
        
        # Initialize population
        self._initialize_population()
        
        logger.info(f"Genetic Algorithm initialized with population size {self.population_size}")
    
    def _initialize_population(self):
        """Create initial random population of deception strategies"""
        self.population = []
        
        for i in range(self.population_size):
            chromosome = self._create_random_chromosome()
            chromosome['id'] = f"gen0_chr{i}"
            self.population.append(chromosome)
        
        logger.info(f"Initialized population with {len(self.population)} chromosomes")
    
    def _create_random_chromosome(self):
        """
        Chromosome represents a complete deception configuration
        Each gene controls a specific deception parameter
        """
        chromosome = {
            # Honeypot configuration genes
            'honeypot_count': random.randint(3, 10),
            'honeypot_types': random.sample(
                ['ssh', 'ftp', 'http', 'mysql', 'redis', 'smtp'], 
                k=random.randint(3, 6)
            ),
            
            # Process mirage genes
            'mirage_config': {
                'count': random.randint(5, 15),
                'mutation_rate': random.uniform(0.1, 0.5),
                'process_types': random.sample(
                    ['database', 'web_server', 'ssh_daemon', 'backup_service', 
                     'cache_server', 'api_gateway', 'file_server', 'mail_server'],
                    k=random.randint(4, 8)
                ),
                'polymorphism_intensity': random.uniform(0.3, 1.0)
            },
            
            # Credential deception genes
            'credential_config': {
                'complexity': random.uniform(0.3, 0.9),
                'realism_level': random.uniform(0.5, 1.0),
                'diversity': random.uniform(0.4, 0.9)
            },
            
            # File system decoy genes
            'filesystem_config': {
                'decoy_density': random.uniform(0.1, 0.8),
                'file_types': random.sample(
                    ['config', 'database', 'backup', 'log', 'key', 'credential'],
                    k=random.randint(3, 6)
                ),
                'fractal_depth': random.randint(2, 5)
            },
            
            # Network behavior genes
            'network_config': {
                'service_diversity': random.randint(3, 10),
                'response_delay': random.uniform(0.1, 2.0),
                'traffic_mimicry': random.uniform(0.5, 1.0)
            },
            
            # Mathematical deception genes
            'math_config': {
                'chaos_parameter': random.uniform(3.6, 4.0),  # Logistic map range
                'entropy_target': random.uniform(0.6, 0.9),
                'fractal_complexity': random.uniform(0.4, 0.9)
            },
            
            # Metadata
            'fitness': 0.0,
            'generation_created': self.generation,
            'parent_ids': []
        }
        
        return chromosome
    
    def fitness_function(self, chromosome, attack_results):
        """
        CORE GA INNOVATION: Fitness measures deception effectiveness
        
        Higher fitness = Better deception strategy
        Components:
        1. Attacker engagement time (longer is better)
        2. Data quality collected (more is better)
        3. Attacker confusion (higher is better)
        4. Genetic diversity (more varied is better)
        """
        if not attack_results:
            return 0.0
        
        # Factor 1: Engagement time (normalize to 0-1)
        engagement_time = attack_results.get('total_interaction_time', 0)
        engagement_score = min(engagement_time / 120.0, 1.0)  # Max 120 seconds
        
        # Factor 2: Data quality
        data_points = attack_results.get('data_points_collected', 0)
        data_score = min(data_points / 100.0, 1.0)  # Max 100 data points
        
        # Factor 3: Confusion metrics
        failed_exploits = attack_results.get('failed_exploits', 0)
        repeated_attempts = attack_results.get('repeated_attempts', 0)
        abandoned = attack_results.get('abandoned', False)
        
        confusion_score = (
            (failed_exploits / max(attack_results.get('total_attempts', 1), 1)) * 0.5 +
            (repeated_attempts / max(attack_results.get('total_attempts', 1), 1)) * 0.3 +
            (0.2 if abandoned else 0.0)
        )
        
        # Factor 4: Genetic diversity
        diversity_score = self._calculate_chromosome_diversity(chromosome)
        
        # Weighted fitness calculation
        weights = self.fitness_weights
        fitness = (
            engagement_score * weights['engagement_time'] +
            data_score * weights['data_quality'] +
            confusion_score * weights['confusion_score'] +
            diversity_score * weights['genetic_diversity']
        )
        
        # Scale to 0-1000 for better visualization
        fitness *= 1000
        
        return fitness
    
    def _calculate_chromosome_diversity(self, chromosome):
        """
        Calculate how diverse/unique this chromosome is
        Higher diversity = more varied deception = harder to predict
        """
        # Entropy of configuration
        config_values = []
        
        # Collect all numerical values
        config_values.append(chromosome['honeypot_count'])
        config_values.append(chromosome['mirage_config']['count'])
        config_values.append(chromosome['mirage_config']['mutation_rate'])
        config_values.append(chromosome['credential_config']['complexity'])
        config_values.append(chromosome['filesystem_config']['decoy_density'])
        config_values.append(chromosome['network_config']['service_diversity'])
        
        # Calculate entropy
        entropy = global_metrics.calculate_entropy(str(config_values))
        
        # Normalize to 0-1
        diversity_score = min(entropy / 10.0, 1.0)
        
        return diversity_score
    
    def evolve_generation(self, attack_results_batch):
        """
        Evolution cycle: Evaluation -> Selection -> Crossover -> Mutation
        
        This is where the magic happens!
        """
        logger.info(f"Evolving generation {self.generation}")
        
        # Step 1: Evaluate fitness for all chromosomes
        fitness_scores = []
        for chromosome in self.population:
            results = attack_results_batch.get(chromosome['id'], {})
            fitness = self.fitness_function(chromosome, results)
            chromosome['fitness'] = fitness
            fitness_scores.append((chromosome, fitness))
        
        # Sort by fitness (descending)
        sorted_population = sorted(fitness_scores, key=lambda x: x[1], reverse=True)
        
        # Track statistics
        best_fitness = sorted_population[0][1]
        avg_fitness = np.mean([f for _, f in fitness_scores])
        worst_fitness = sorted_population[-1][1]
        
        # Step 2: Elitism - preserve top performers
        new_population = [chrom for chrom, fit in sorted_population[:self.elite_size]]
        
        logger.info(f"Elite chromosomes preserved: {self.elite_size}")
        
        # Step 3: Selection for breeding (Tournament selection)
        breeding_pool = self._tournament_selection(sorted_population, self.population_size // 2)
        
        # Step 4: Crossover - create offspring
        offspring = []
        while len(new_population) + len(offspring) < self.population_size:
            if len(breeding_pool) < 2:
                break
            
            parent1 = random.choice(breeding_pool)
            parent2 = random.choice(breeding_pool)
            
            if random.random() < self.crossover_rate:
                child1, child2 = self._crossover(parent1, parent2)
                offspring.extend([child1, child2])
            else:
                offspring.extend([copy.deepcopy(parent1), copy.deepcopy(parent2)])
        
        # Step 5: Mutation - introduce variations
        for child in offspring:
            if random.random() < self.mutation_rate:
                child = self._mutate(child)
        
        # Step 6: Form new population
        new_population.extend(offspring[:self.population_size - len(new_population)])
        self.population = new_population
        
        # Update generation counter
        self.generation += 1
        
        # Log evolution event
        evolution_data = {
            'generation': self.generation,
            'best_fitness': best_fitness,
            'avg_fitness': avg_fitness,
            'worst_fitness': worst_fitness,
            'best_chromosome': sorted_population[0][0],
            'improvement': best_fitness - self.fitness_history[-1]['best_fitness'] if self.fitness_history else 0.0
        }
        
        self.fitness_history.append(evolution_data)
        self.best_chromosome_history.append(sorted_population[0][0])
        
        deception_logger.log_genetic_evolution(evolution_data)
        
        logger.info(f"Generation {self.generation} complete: Best Fitness = {best_fitness:.2f}, Avg = {avg_fitness:.2f}")
        
        return sorted_population[0][0]  # Return best chromosome
    
    def _tournament_selection(self, sorted_population, tournament_size):
        """Tournament selection for breeding"""
        selected = []
        population_size = len(sorted_population)
        
        for _ in range(tournament_size):
            # Randomly select k individuals for tournament
            k = 3  # Tournament size
            tournament = random.sample(sorted_population, k)
            
            # Select the best from tournament
            winner = max(tournament, key=lambda x: x[1])[0]
            selected.append(winner)
        
        return selected
    
    def _crossover(self, parent1, parent2):
        """
        Crossover: Combine genetic material from two parents
        
        Strategy: Blend genes from both parents
        """
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        
        # Crossover honeypot config
        if random.random() < 0.5:
            child1['honeypot_count'] = parent2['honeypot_count']
            child2['honeypot_count'] = parent1['honeypot_count']
        
        # Crossover mirage config
        if random.random() < 0.5:
            child1['mirage_config']['count'] = parent2['mirage_config']['count']
            child2['mirage_config']['count'] = parent1['mirage_config']['count']
        
        # Crossover credentials
        if random.random() < 0.5:
            child1['credential_config'] = copy.deepcopy(parent2['credential_config'])
            child2['credential_config'] = copy.deepcopy(parent1['credential_config'])
        
        # Crossover filesystem
        if random.random() < 0.5:
            child1['filesystem_config'] = copy.deepcopy(parent2['filesystem_config'])
            child2['filesystem_config'] = copy.deepcopy(parent1['filesystem_config'])
        
        # Blend numerical values
        for config_key in ['network_config', 'math_config']:
            for param_key in child1[config_key].keys():
                if isinstance(child1[config_key][param_key], (int, float)):
                    # Blend with random weight
                    alpha = random.random()
                    child1[config_key][param_key] = (
                        alpha * parent1[config_key][param_key] +
                        (1 - alpha) * parent2[config_key][param_key]
                    )
                    child2[config_key][param_key] = (
                        (1 - alpha) * parent1[config_key][param_key] +
                        alpha * parent2[config_key][param_key]
                    )
        
        # Update metadata
        child1['id'] = f"gen{self.generation}_chr{random.randint(1000,9999)}"
        child2['id'] = f"gen{self.generation}_chr{random.randint(1000,9999)}"
        child1['parent_ids'] = [parent1['id'], parent2['id']]
        child2['parent_ids'] = [parent1['id'], parent2['id']]
        child1['generation_created'] = self.generation
        child2['generation_created'] = self.generation
        
        return child1, child2
    
    def _mutate(self, chromosome):
        """
        Mutation: Random changes to genes
        Introduces variation and prevents premature convergence
        """
        mutated = copy.deepcopy(chromosome)
        
        # Mutate honeypot count
        if random.random() < 0.3:
            mutated['honeypot_count'] += random.randint(-2, 2)
            mutated['honeypot_count'] = max(3, min(10, mutated['honeypot_count']))
        
        # Mutate mirage config
        if random.random() < 0.3:
            mutated['mirage_config']['count'] += random.randint(-3, 3)
            mutated['mirage_config']['count'] = max(5, min(15, mutated['mirage_config']['count']))
        
        if random.random() < 0.3:
            mutated['mirage_config']['mutation_rate'] += random.uniform(-0.1, 0.1)
            mutated['mirage_config']['mutation_rate'] = max(0.1, min(0.5, mutated['mirage_config']['mutation_rate']))
        
        # Mutate credential config
        for param in ['complexity', 'realism_level', 'diversity']:
            if random.random() < 0.3:
                mutated['credential_config'][param] += random.uniform(-0.1, 0.1)
                mutated['credential_config'][param] = max(0.0, min(1.0, mutated['credential_config'][param]))
        
        # Mutate filesystem config
        if random.random() < 0.3:
            mutated['filesystem_config']['decoy_density'] += random.uniform(-0.1, 0.1)
            mutated['filesystem_config']['decoy_density'] = max(0.1, min(0.8, mutated['filesystem_config']['decoy_density']))
        
        # Mutate network config
        if random.random() < 0.3:
            mutated['network_config']['service_diversity'] += random.randint(-2, 2)
            mutated['network_config']['service_diversity'] = max(3, min(10, mutated['network_config']['service_diversity']))
        
        # Mutate math config
        if random.random() < 0.3:
            mutated['math_config']['chaos_parameter'] += random.uniform(-0.1, 0.1)
            mutated['math_config']['chaos_parameter'] = max(3.6, min(4.0, mutated['math_config']['chaos_parameter']))
        
        logger.debug(f"Mutation applied to chromosome {chromosome['id']}")
        
        return mutated
    
    def get_best_chromosome(self):
        """Get the current best deception strategy"""
        if not self.population:
            return None
        
        return max(self.population, key=lambda x: x.get('fitness', 0))
    
    def get_evolution_stats(self):
        """Get evolution statistics for visualization"""
        if not self.fitness_history:
            return {
                'generation': 0,
                'best_fitness': 0.0,
                'avg_fitness': 0.0,
                'improvement_rate': 0.0
            }
        
        latest = self.fitness_history[-1]
        
        # Calculate improvement rate
        if len(self.fitness_history) > 1:
            first_gen = self.fitness_history[0]['best_fitness']
            current_gen = latest['best_fitness']
            improvement_rate = ((current_gen - first_gen) / first_gen * 100) if first_gen > 0 else 0.0
        else:
            improvement_rate = 0.0
        
        return {
            'generation': latest['generation'],
            'best_fitness': latest['best_fitness'],
            'avg_fitness': latest['avg_fitness'],
            'improvement_rate': improvement_rate,
            'total_generations': len(self.fitness_history)
        }
    
    def export_best_strategy(self):
        """Export the best deception strategy for deployment"""
        best = self.get_best_chromosome()
        if not best:
            return None
        
        return {
            'strategy_id': best['id'],
            'fitness_score': best['fitness'],
            'generation': best['generation_created'],
            'configuration': {
                'honeypots': {
                    'count': best['honeypot_count'],
                    'types': best['honeypot_types']
                },
                'mirages': best['mirage_config'],
                'credentials': best['credential_config'],
                'filesystem': best['filesystem_config'],
                'network': best['network_config'],
                'mathematics': best['math_config']
            }
        }