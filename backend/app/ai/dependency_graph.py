"""
Dependency Graph - Builds and manages skill dependency relationships
"""
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque
import networkx as nx


class DependencyGraph:
    """
    Builds and traverses skill dependency graph using graph algorithms
    """
    
    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.skill_categories = self._initialize_category_map()
    
    def _initialize_category_map(self) -> Dict[str, List[str]]:
        """Map categories to their typical dependencies"""
        return {
            'programming_languages': [],
            'frameworks_libraries': ['programming_languages'],
            'databases': ['programming_languages'],
            'cloud_platforms': ['devops_tools'],
            'devops_tools': ['programming_languages', 'databases'],
            'ml_ai': ['programming_languages', 'data_engineering'],
            'data_engineering': ['programming_languages', 'databases'],
            'soft_skills': []
        }
    
    def build_graph(
        self,
        skills: List[str],
        categories: Dict[str, str],
        explicit_dependencies: Optional[Dict[str, List[str]]] = None
    ) -> nx.DiGraph:
        """
        Build directed graph of skill dependencies
        """
        self.graph.clear()
        
        for skill in skills:
            category = categories.get(skill, 'uncategorized')
            self.graph.add_node(skill, category=category)
            
            implicit_deps = self.skill_categories.get(category, [])
            for dep in implicit_deps:
                if dep in skills:
                    self.graph.add_edge(dep, skill)
        
        if explicit_dependencies:
            for skill, deps in explicit_dependencies.items():
                for dep in deps:
                    if dep in skills:
                        self.graph.add_edge(dep, skill)
        
        return self.graph
    
    def get_learning_order(self) -> List[str]:
        """
        Topological sort to get optimal learning order
        Respects dependencies
        """
        try:
            return list(nx.topological_sort(self.graph))
        except nx.NetworkXError:
            return self._handle_cycles()
    
    def _handle_cycles(self) -> List[str]:
        """Handle circular dependencies by breaking smallest edges"""
        try:
            cycle = nx.find_cycle(self.graph)
            
            edges_to_remove = []
            for edge in cycle:
                weight = self._get_cycle_break_weight(edge)
                edges_to_remove.append((weight, edge))
            
            edges_to_remove.sort()
            _, break_edge = edges_to_remove[0]
            
            self.graph.remove_edge(*break_edge)
            
            return self.get_learning_order()
            
        except nx.NetworkXNoCycle:
            return list(nx.topological_sort(self.graph))
    
    def _get_cycle_break_weight(self, edge: Tuple[str, str]) -> float:
        """Determine which edge to break in a cycle"""
        skill1, skill2 = edge
        return len(skill1) + len(skill2)
    
    def get_prerequisites(self, skill: str) -> List[str]:
        """Get immediate prerequisites for a skill"""
        predecessors = list(self.graph.predecessors(skill))
        return predecessors
    
    def get_all_prerequisites(self, skill: str) -> Set[str]:
        """Get all prerequisites (transitive closure)"""
        ancestors = nx.ancestors(self.graph, skill)
        return ancestors
    
    def get_dependents(self, skill: str) -> List[str]:
        """Get skills that depend on this skill"""
        return list(self.graph.successors(skill))
    
    def get_learnable_skills(
        self, 
        learned_skills: Set[str],
        target_skills: Set[str]
    ) -> List[str]:
        """
        Get skills that can be learned now (all prerequisites satisfied)
        """
        learnable = []
        
        for skill in target_skills:
            if skill in learned_skills:
                continue
            
            prereqs = self.get_all_prerequisites(skill)
            
            if prereqs.issubset(learned_skills):
                learnable.append(skill)
        
        learnable.sort(key=lambda s: self._get_skill_priority(s, learned_skills))
        
        return learnable
    
    def _get_skill_priority(self, skill: str, learned: Set[str]) -> float:
        """Calculate priority for learnable skill"""
        dependents = self.get_dependents(skill)
        dependent_count = sum(
            1 for d in dependents 
            if d not in learned and self.get_all_prerequisites(d).issubset(learned | {skill})
        )
        
        return -dependent_count
    
    def compute_learning_path(
        self,
        start_skills: Set[str],
        target_skills: Set[str],
        max_depth: int = 10
    ) -> List[List[str]]:
        """
        Compute multiple learning paths to reach target skills
        """
        paths = []
        
        for target in target_skills:
            if target in start_skills:
                continue
            
            path = self._find_learning_path(start_skills, target, max_depth)
            if path:
                paths.append(path)
        
        paths.sort(key=len)
        
        return paths
    
    def _find_learning_path(
        self,
        start: Set[str],
        target: str,
        max_depth: int
    ) -> List[str]:
        """BFS to find shortest learning path"""
        queue = deque([(list(start), [target])])
        visited = {frozenset(start)}
        
        while queue:
            current, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            prereqs = self.get_prerequisites(path[-1])
            
            if not prereqs or any(p in current for p in prereqs):
                return path
            
            for prereq in prereqs:
                if prereq not in current:
                    new_state = frozenset(current + [prereq])
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((current + [prereq], path + [prereq]))
        
        return path if 'path' in locals() else []
    
    def get_skill_clusters(self) -> List[List[str]]:
        """
        Identify skill clusters (skills that can be learned in parallel)
        """
        undirected = self.graph.to_undirected()
        
        try:
            components = list(nx.connected_components(undirected))
            return [list(comp) for comp in components]
        except:
            return [[s] for s in self.graph.nodes()]
    
    def visualize_dependencies(self) -> Dict:
        """Export graph data for visualization"""
        nodes = []
        edges = []
        
        for node in self.graph.nodes():
            nodes.append({
                'id': node,
                'category': self.graph.nodes[node].get('category', 'uncategorized'),
                'level': nx.shortest_path_length(
                    self.graph, 
                    source=min(self.graph.nodes(), key=lambda x: nx.shortest_path_length(self.graph, source=x, target=node) if nx.has_path(self.graph, x, node) else float('inf'))
                ) if self.graph.nodes() else 0
            })
        
        for edge in self.graph.edges():
            edges.append({
                'source': edge[0],
                'target': edge[1]
            })
        
        return {'nodes': nodes, 'edges': edges}
