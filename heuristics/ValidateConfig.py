import os

# Validate config attributes read from a DAT file.
class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['inputDataFile', 'solutionFile', 'solver']:
            if(not data.__dict__.has_key(paramName)):
                raise Exception('Parameter/Set(%s) not contained in Configuration' % str(paramName))

        # Validate input data file
        inputDataFile = data.inputDataFile
        if(len(inputDataFile) == 0):
            raise Exception('Value for inputDataFile is empty')
        if(not os.path.exists(inputDataFile)):
            raise Exception('inputDataFile(%s) does not exist' % inputDataFile)
        
        # Validate solution file
        solutionFile = data.solutionFile
        if(len(solutionFile) == 0):
            raise Exception('Value for solutionFile is empty')
        
        # Validate verbose
        verbose = False
        if(data.__dict__.has_key('verbose')):
            verbose = data.verbose
            if(not isinstance(verbose, (bool)) or (verbose not in [True, False])):
                raise Exception('verbose(%s) has to be a boolean value.' % str(verbose))
        else:
            data.verbose = verbose
        
        # Validate solver and per-solver parameters
        solver = data.solver
        if(solver == 'Greedy'):
            # Validate that mandatory input parameters for Greedy solver were found
            for paramName in ['localSearch']:
                if(not data.__dict__.has_key(paramName)):
                    raise Exception('Parameter/Set(%s) not contained in Configuration. Required by Greedy solver.' % str(paramName))

            # Validate localSearch
            localSearch = data.localSearch
            if(not isinstance(localSearch, (bool)) or (localSearch not in [True, False])):
                raise Exception('localSearch(%s) has to be a boolean value.' % str(localSearch))

        elif(solver == 'GRASP'):
            # Validate that mandatory input parameters for GRASP solver were found
            for paramName in ['maxExecTime', 'alpha', 'localSearch']:
                if(not data.__dict__.has_key(paramName)):
                    raise Exception('Parameter/Set(%s) not contained in Configuration. Required by GRASP solver.' % str(paramName))

            # Validate maxExecTime
            maxExecTime = data.maxExecTime
            if(not isinstance(maxExecTime, (int, long, float)) or (maxExecTime <= 0)):
                raise Exception('maxExecTime(%s) has to be a positive float value.' % str(maxExecTime))

            # Validate alpha
            alpha = data.alpha
            if(not isinstance(alpha, (int, long, float)) or (alpha < 0) or (alpha > 1)):
                raise Exception('alpha(%s) has to be a float value in range [0, 1].' % str(alpha))

            # Validate localSearch
            localSearch = data.localSearch
            if(not isinstance(localSearch, (bool)) or (localSearch not in [True, False])):
                raise Exception('localSearch(%s) has to be a boolean value.' % str(localSearch))

        elif(solver == 'BRKGA'):
            # Validate that mandatory input parameters for BRKGA solver were found
            for paramName in ['maxExecTime', 'numIndividuals', 'pElites', 'pMutants', 'pInheritanceElite']:
                if(not data.__dict__.has_key(paramName)):
                    raise Exception('Parameter/Set(%s) not contained in Configuration. Required by BRKGA solver.' % str(paramName))
            
            # Validate maxExecTime
            maxExecTime = data.maxExecTime
            if(not isinstance(maxExecTime, (int, long, float)) or (maxExecTime <= 0)):
                raise Exception('maxExecTime(%s) has to be a positive float value.' % str(maxExecTime))

            # Validate numIndividuals
            numIndividuals = data.numIndividuals
            if(not isinstance(numIndividuals, (int, long)) or (numIndividuals <= 0)):
                raise Exception('numIndividuals(%s) has to be a strictly positive integer value.' % str(numIndividuals))

            # Validate pElites
            pElites = data.pElites
            if(not isinstance(pElites, (int, long, float)) or (pElites < 0) or (pElites > 1)):
                raise Exception('pElites(%s) has to be a float value in range [0, 1].' % str(pElites))

            # Validate pMutants
            pMutants = data.pMutants
            if(not isinstance(pMutants, (int, long, float)) or (pMutants < 0) or (pMutants > 1)):
                raise Exception('pMutants(%s) has to be a float value in range [0, 1].' % str(pMutants))

            # Validate pInheritanceElite
            pInheritanceElite = data.pInheritanceElite
            if(not isinstance(pInheritanceElite, (int, long, float)) or (pInheritanceElite < 0) or (pInheritanceElite > 1)):
                raise Exception('pInheritanceElite(%s) has to be a float value in range [0, 1].' % str(pInheritanceElite))

            # local search not used in BRKGA. Disable it.
            localSearch = False
            if(data.__dict__.has_key('localSearch')):
                localSearch = data.localSearch
                if(not isinstance(localSearch, (bool)) or (localSearch not in [True, False])):
                    raise Exception('localSearch(%s) has to be a boolean value.' % str(localSearch))
                
                if(localSearch):
                    print('localSearch was enabled in BRKGA. Disabling it.')
            
            data.localSearch = False

        else:
            raise Exception('Unsupported solver specified(%s) in Configuration. Supported solvers are: Greedy, GRASP and BRKGA.' % str(solver))
        
        if(data.localSearch):
            # Validate that mandatory input parameters for local search were found
            for paramName in ['neighborhoodStrategy', 'policy']:
                if(not data.__dict__.has_key(paramName)):
                    raise Exception('Parameter/Set(%s) not contained in Configuration. Required by Local Search.' % str(paramName))

            # Validate neighborhoodStrategy
            neighborhoodStrategy = data.neighborhoodStrategy
            if(neighborhoodStrategy not in ['Reassignment', 'Exchange']):
                raise Exception('neighborhoodStrategy(%s) has to be one of [Reassignment, Exchange].' % str(neighborhoodStrategy))

            # Validate policy
            policy = data.policy
            if(policy not in ['BestImprovement', 'FirstImprovement']):
                raise Exception('policy(%s) has to be one of [BestImprovement, FirstImprovement].' % str(policy))
