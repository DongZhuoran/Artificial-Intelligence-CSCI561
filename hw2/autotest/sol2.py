# -*- coding: utf-8 -*-
import time
import copy
import sys


def main(argv):
    global max_dec
    # Get pointers of input & output files
    try:
        fp = open('./cases/input' + str(argv[0]) + '.txt', 'r')
        resf = open('./cases/output' + str(argv[0]) + '.txt', 'r')
    except IOError:
        return
    output = open('output' + str(argv[1]) + '.txt', 'w')

    # Load parameters
    num_lahsa = int(fp.readline())
    num_spla = int(fp.readline())
    num_lahsa_chosen = int(fp.readline())
    lahsa_chosen = []
    for i in xrange(num_lahsa_chosen):
        lahsa_chosen.append(fp.readline().strip())
    num_spla_chosen = int(fp.readline())
    spla_chosen = []
    for i in xrange(num_spla_chosen):
        spla_chosen.append(fp.readline().strip())
    num_applicants = int(fp.readline())
    applicants = []
    applicants_lahsa = []
    applicants_spla = []
    for i in xrange(num_applicants):
        applicant = fp.readline().strip()
        applicants.append(applicant)
        if is_lahsa_valid(applicant) and applicant[0:5] not in lahsa_chosen and \
                applicant[0:5] not in spla_chosen:
            val = 0
            for j in xrange(7):
                val = val + int(applicant[13+j:14+j])
            applicants_lahsa.append((applicant, val))
        if is_spla_valid(applicant) and applicant[0:5] not in lahsa_chosen and \
                applicant[0:5] not in spla_chosen:
            val = 0
            for j in xrange(7):
                val = val + int(applicant[13+j:14+j])
            applicants_spla.append((applicant, val))

    positions_lahsa = [num_lahsa] * 7
    positions_spla = [num_spla] * 7
    init_positions(positions_lahsa, positions_spla, lahsa_chosen,
                   spla_chosen, applicants)
    # print positions_lahsa, positions_spla  # test
    max_dec = {}
    applicant_next = minimax_decision(applicants_lahsa, applicants_spla,
                                positions_lahsa, positions_spla)
    # print applicant_next
    if applicant_next == resf.readline().strip():
        print 'case ' + str(argv[0]) + ' passes'
    else:
        print 'case ' + str(argv[0]) + ' failed'
    output.write(applicant_next)
    fp.close()
    output.close()


def minimax_decision(applicants_lahsa, applicants_spla, positions_lahsa, positions_spla):
    lahsa_val = -1
    spla_val = -1
    applicant_next = ''
    for applicant in applicants_spla:
        if is_compatible(positions_spla, applicant[0]):
            applicants_spla_new = copy.deepcopy(applicants_spla)
            applicants_lahsa_new = copy.deepcopy(applicants_lahsa)
            positions_lahsa_new = copy.deepcopy(positions_lahsa)
            positions_spla_new = copy.deepcopy(positions_spla)
            applicants_spla_new.remove(applicant)
            choose_applicant(positions_spla_new, applicant[0])
            if applicant in applicants_lahsa:
                applicants_lahsa_new.remove(applicant)
            val = min_value(applicants_lahsa_new, applicants_spla_new,
                            positions_lahsa_new, positions_spla_new, True)
            if applicant[1] + val[1] > spla_val:
                lahsa_val = val[0]
                spla_val = applicant[1] + val[1]
                applicant_next = applicant[0][0:5]
            # Take competition into consideration.
            # if applicant[1] +val[1] == spla_val:
            #     if lahsa_val >= val[0]:
            #         lahsa_val = val[0]
            #         spla_val = applicant[1] + val[1]
            #         applicant_next = applicant[0][0:5]
    # print 'lahsa_val: %s, spla_val: %s' % (lahsa_val, spla_val)
    return applicant_next


def max_value(applicants_lahsa, applicants_spla, positions_lahsa, positions_spla, is_lahsa_compatible):
    global max_dec
    key = generate_key(positions_lahsa, positions_spla, applicants_lahsa, applicants_spla)
    if key in max_dec:
        return max_dec[key]
    lahsa_val = -1
    spla_val = -1
    is_spla_compatible = False
    for applicant in applicants_spla:
        if is_compatible(positions_spla, applicant[0]):
            is_spla_compatible = True
            applicants_lahsa_new = copy.deepcopy(applicants_lahsa)
            applicants_spla_new = copy.deepcopy(applicants_spla)
            positions_lahsa_new = copy.deepcopy(positions_lahsa)
            positions_spla_new = copy.deepcopy(positions_spla)
            applicants_spla_new.remove(applicant)
            choose_applicant(positions_spla_new, applicant[0])
            if applicant in applicants_lahsa:
                applicants_lahsa_new.remove(applicant)
            val = min_value(applicants_lahsa_new, applicants_spla_new,
                            positions_lahsa_new, positions_spla_new, True)
            # todo: take the id into consideration when the values are equal.
            if applicant[1] + val[1] > spla_val:
                lahsa_val = val[0]
                spla_val = applicant[1] + val[1]
            # Take competition into consideration.
            # if applicant[1] + val[1] == spla_val:
            #     if lahsa_val >= val[0]:
            #         lahsa_val = val[0]
            #         spla_val = applicant[1] + val[1]
    if not is_spla_compatible:
        if not is_lahsa_compatible:
            max_dec[key] = [0, 0]
            return 0, 0
        return min_value(applicants_lahsa, applicants_spla, positions_lahsa, positions_spla, False)
    max_dec[key] = [lahsa_val, spla_val]
    return lahsa_val, spla_val


def min_value(applicants_lahsa, applicants_spla, positions_lahsa, positions_spla, is_spla_compatible):
    global max_dec
    key = generate_key(positions_lahsa, positions_spla, applicants_lahsa, applicants_spla)
    if key in max_dec:
        return max_dec[key]
    lahsa_val = -1
    spla_val = -1
    is_lahsa_compatible = False
    for applicant in applicants_lahsa:
        if is_compatible(positions_lahsa, applicant[0]):
            is_lahsa_compatible = True
            applicants_lahsa_new = copy.deepcopy(applicants_lahsa)
            applicants_spla_new = copy.deepcopy(applicants_spla)
            positions_lahsa_new = copy.deepcopy(positions_lahsa)
            positions_spla_new = copy.deepcopy(positions_spla)
            applicants_lahsa_new.remove(applicant)
            choose_applicant(positions_lahsa_new, applicant[0])
            if applicant in applicants_spla:
                applicants_spla_new.remove(applicant)
            val = max_value(applicants_lahsa_new, applicants_spla_new,
                            positions_lahsa_new, positions_spla_new, True)
            # todo: take the id into consideration when the values are equal.
            if applicant[1] + val[0] > lahsa_val:
                lahsa_val = applicant[1] + val[0]
                spla_val = val[1]
            # Take competition into consideration.
            # if applicant[1] + val[0] == lahsa_val:
            #     if spla_val >= val[1]:
            #         lahsa_val = applicant[1] + val[0]
            #         spla_val = val[1]
    if not is_lahsa_compatible:
        if not is_spla_compatible:
            max_dec[key] = [0, 0]
            return 0, 0
        return max_value(applicants_lahsa, applicants_spla, positions_lahsa, positions_spla, False)
    max_dec[key] = [lahsa_val, spla_val]
    return lahsa_val, spla_val


def generate_key(positions_lahsa, positions_spla, applicants_lahsa, applicants_spla):
    positions = ''.join(str(pos) for pos in positions_lahsa) + ''.join(str(pos) for pos in positions_spla)
    applicants = ''.join(appId[0][0:5] for appId in applicants_lahsa) + ''.join(appId[0][0:5] for appId in applicants_spla)
    return positions + applicants


def init_positions(positions_lahsa, positions_spla, lahsa_chosen,
                   spla_chosen, applicants):
    # Initialize LAHSA's positions.
    for id in lahsa_chosen:
        for applicant in applicants:
            if id == applicant[0:5]:
                positions_lahsa = choose_applicant(positions_lahsa, applicant)

    # Initialize SPLA's positions.
    for id in spla_chosen:
        for applicant in applicants:
            if id == applicant[0:5]:
                positions_spla = choose_applicant(positions_spla, applicant)


def choose_applicant(positions, applicant):
    for i in xrange(len(positions)):
        positions[i] = positions[i] - int(applicant[13+i:14+i])
    return positions


def is_compatible(positions, applicant):
    '''
    Check whether resources are enough.
    :param positions: The rest positions of a given organization.
    :param applicant: A piece of applicant info.
    :return: True for enough, False otherwise.
    '''
    if isinstance(applicant, list):
        positions_temp = copy.deepcopy(positions)
        for a in applicant:
            if is_compatible(positions_temp, a):
                choose_applicant(positions_temp, a)
            else:
                return False
    else:
        for i in xrange(len(positions)):
            if positions[i] - int(applicant[13+i:14+i]) < 0:
                return False
    return True


def is_lahsa_valid(applicant):
    '''
    Check whether it is a valid LAHSA applicant.
    :param applicant: A piece of applicant info.
    :return: True for valid, False otherwise.
    '''
    gender = applicant[5:6]
    age = int(applicant[6:9])
    has_pets = applicant[9:10]
    return (gender == 'F') and (age > 17) and (has_pets == 'N')


def is_spla_valid(applicant):
    '''
    Check whether it is a valid SPLA applicant.
    :param applicant: A piece of applicant info
    :return: True for valid, False otherwise.
    '''
    has_medical_condition = applicant[10:11]
    has_car = applicant[11:12]
    has_license = applicant[12:13]
    return (has_medical_condition == 'N') and (has_car == 'Y') and (has_license == 'Y')


if __name__ == '__main__':
	try:
		if len(sys.argv) != 2:
			print 'There should be 2 arguments.'
		else:
			start_time = time.time()
			main(sys.argv)
			print "%s seconds" % (time.time() - start_time)
	except IOError:
		pass