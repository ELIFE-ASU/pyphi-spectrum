#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# phi_spectrum.py

"""Wrapper to calculate the entire spectrum of Phi values for each cut of a given subsystem"""

import numpy as np
import itertools
from .direction import Direction
# from .subsystem import potential_purviews,find_mip
from .utils import powerset
from .models import MaximallyIrreducibleCause, MaximallyIrreducibleEffect, Concept, CauseEffectStructure
from .compute.distance import ces_distance
from .compute.subsystem import sia_bipartitions

## Find all concepts for the specified subsystem
def get_all_concepts(subsystem):
	all_concepts = []
	mechanisms = powerset(subsystem.node_indices, nonempty=True)
	for mechanism in mechanisms:
		mechanism_concepts = []
		
		# Find the CORE cause(s) for a given mechanism
		direction = Direction.CAUSE
		past_purviews = subsystem.potential_purviews(direction, mechanism, purviews=False)
		all_causes = [subsystem.find_mip(direction, mechanism, purview) for purview in past_purviews]
		core_cause = max(all_causes)
		if core_cause.phi > 0.:
			all_core_causes = [value for index,value in enumerate(subsystem.find_mip(direction, mechanism, purview) for purview in past_purviews) if value.phi == core_cause.phi]
		else:
			all_core_causes = [core_cause]
					
		# Find the CORE effect(s) for a given mechanism
		direction = Direction.EFFECT
		future_purviews = subsystem.potential_purviews(direction, mechanism, purviews=False)
		all_effects = [subsystem.find_mip(direction, mechanism, purview) for purview in future_purviews]
		core_effect = max(all_effects)
		if core_effect.phi > 0.:
			all_core_effects = [value for index,value in enumerate(subsystem.find_mip(direction, mechanism, purview) for purview in future_purviews) if value.phi == core_effect.phi]
		else:
			all_core_effects = [core_effect]
				
				
		## Now we need to build concepts for all possible core cause and core effect combinations
		for each_cause in all_core_causes:
			MIC = MaximallyIrreducibleCause(each_cause)
			for each_effect in all_core_effects:
				MIE = MaximallyIrreducibleEffect(each_effect)
				
				concept = Concept(mechanism = mechanism, cause = MIC, effect = MIE, subsystem = subsystem)            
								
				## If phi^max > 0 store the concept
				if concept.phi > 0.:
					mechanism_concepts.append(concept)
				
		if mechanism_concepts:
			all_concepts.append(mechanism_concepts)

	return(all_concepts)


## Generate all possible cause-effect structures (CES) using the list of all concepts
def get_all_CES(all_concepts):
	all_CES = []

	## Get the cartesian product of all possible concepts for each mechanism
	for element in itertools.product(*all_concepts):
		all_CES.append(CauseEffectStructure(concepts=element))

	return(all_CES)

## Return the spectrum of Phi values
def get_phi_spectrum(subsystem,display_CES=False):

	## Initialize an empty list to store all Phi values for all cuts
	Phi_Spectrum = []

	## Find all concepts for the specified subsystem
	all_concepts = get_all_concepts(subsystem)

	## Create all possible cause-effect structures (CES) via the cartesian product of all concepts for each mechanism
	original_CES = get_all_CES(all_concepts)

	print("\tNumber of Non-unique Constellations =",len(original_CES))
	if display_CES:
		print(original_CES)


	## Now cut the original TPM and find the new set of concepts. Get the Phi value and repeat the cut
	bipartitions = sia_bipartitions(subsystem.cut_indices, subsystem.cut_node_labels)
	for cut in bipartitions:
		print("\nEvaluating Cut ",cut)
		new_subsystem = subsystem.apply_cut(cut)
		
		## Find all concepts for the specified subsystem
		new_concepts = get_all_concepts(new_subsystem)
		new_CES = get_all_CES(new_concepts)

		print("\tNumber of Non-unique Constellations =",len(new_CES))
		if display_CES:
			print(new_CES)

		## Now store all possible Phi values for this cut
		Phi_cut = []
		for original in original_CES:
			for new in new_CES:
				Phi = ces_distance(original,new)
				Phi_cut.append(Phi)
				
		## Append the list of Phi values to the spectrum
		print("\tPhi Values for Cut = ",Phi_cut)
		Phi_Spectrum.append(Phi_cut)

	return(bipartitions,Phi_Spectrum)

## Return all Phi values between the min and max Phi value of the MIP
def get_Phi_MIP(phi_spectrum):

	cuts = phi_spectrum[0]
	values = phi_spectrum[1]

	## Get the minimum Phi value of the MIP
	Phi_min_MIP = np.min(values[0])
	for each in values:
	    if np.min(each) < Phi_min_MIP:
	        Phi_min_MIP = np.min(each)
	        
	        
	## Get the list(s) of Phi values corresponding to possible MIPS
	possible_MIPs = (index for index in values if np.min(index) == Phi_min_MIP)


	## Upper bound on Phi is the smallest of the max Phi values
	Phi_max_MIP = np.max(values[0])
	for each in possible_MIPs:
	    if np.max(each) < Phi_max_MIP:
	        Phi_max_MIP = np.max(each)

    ## Return all Phi values between Phi_min_MIP and Phi_max_MIP
	valid_phi = [phi for index in values for phi in index if phi >= Phi_min_MIP and phi <= Phi_max_MIP]
	return(np.unique(valid_phi))



