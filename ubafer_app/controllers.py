import math, time
from datetime import timedelta, datetime


def get_track_wise_talk_details(test_input, output_file):
    """
    function to get track wise details for all the talks
    1. first setting the variables as needed
    2. calling function for getting the total count , index wise dictionary, time wise dict of data and lightning
     event count
    3. setting the total number of track need to make and copying the time dict for tempoary use to manipulate
    4. writing the needed things in the file for output purpose
    5. calling the files function for getting the details for each and every track
    6. after getting the track calling the function for getting the output for each and evry track one by one
    7. inserting data into file for output purpose.
    :param test_input: input files
    :param output_file: text input file for showing output
    :return:
    """
    res_list = {}
    try:
        first_half = 180
        second_half = 240
        half_tot = 420
        inc_counter = 0
        tot, ind_dict, time_dict, light_count = get_index_wise_time_bassed_list(test_input)
        event_tot = math.ceil(tot / half_tot)
        temp_dict = time_dict.copy()
        for e in range(event_tot):
            # print('Track ', e + 1)
            output_file.write('Track ' + str(e+1) + '\n')
            track = get_track_details(first_half, second_half, temp_dict)
            new_temp_dict = time_dict.copy()
            out_list = get_track_output_list(track, time_dict, new_temp_dict, ind_dict, test_input,
                                             inc_counter, event_tot, light_count)
            for i in out_list:
                # print(i)
                output_file.write(str(i) + '\n')
            output_file.write('\n')
            res_list['Track ' + str(e + 1)] = out_list
    except Exception as e:
        print(e.args)
    return res_list


def get_track_output_list(track, time_dict, new_temp_dict, ind_dict, test_input, inc_counter, event_tot, light_count):
    """
    function for getting the track output file data .
    1. first setting the variables for timedelta
    2. now iterating through the track list and getting index and finding the actual value for that index.
    3.  checking for lunch time and then updating the output accordingly
    4. checking for lightning is present or not if present then making the outlist accordingly , after that
        checking for time insertion for netwroking
    :param track: track list c
    :param time_dict: time wise dict for data
    :param new_temp_dict: temp dict for manipulating
    :param ind_dict: index wise dict
    :param test_input: input list with all data
    :param inc_counter: increment counter
    :param event_tot: total of event/track need to make
    :param light_count: count of lightning event present
    :return:
    """
    out_list = []
    try:
        cur_time = timedelta(hours=9)
        lunch_time = timedelta(hours=12)
        evening_time = timedelta(hours=17)
        for t in track:
            ind_val = time_dict.get(t) - new_temp_dict.get(t)
            main_ind = ind_dict.get(t)[ind_val]
            new_temp_dict[t] -= 1
            text = test_input[main_ind]
            t_time = timedelta(minutes=t)
            if cur_time + t_time == lunch_time:
                out_list.append((datetime.min + cur_time).strftime(('%I:%M%p')) + '  ' + text)
                out_list.append((datetime.min + lunch_time).strftime(('%I:%M%p')) + '  Lunch')
                cur_time += timedelta(minutes=60)
            else:
                out_list.append((datetime.min + cur_time).strftime(('%I:%M%p')) + '  ' + text)
            cur_time += t_time
        if inc_counter == event_tot - 1 and 'lightning' in ind_dict:
            if cur_time < evening_time:
                for i in range(light_count):
                    out_list.append((datetime.min + cur_time).strftime(('%I:%M%p')) + '  ' + test_input[
                        ind_dict.get('lightning')[i]])
                    cur_time += timedelta(minutes=5)
                diff_time = evening_time - cur_time
                seconds = diff_time.seconds
                if diff_time.seconds > 3600:
                    seconds = diff_time.seconds - 3600
                cur_time += timedelta(seconds=seconds)
        out_list.append((datetime.min + cur_time).strftime(('%I:%M%p')) + '  ' + 'Networking Event')
        inc_counter += 1
    except Exception as e:
        print(e.args)
    return out_list


def get_track_details(first_half, second_half, temp_dict):
    """
    function to get the track details for first half and second half
    1. calling the while loop for getting the data for first half and when it come to lunch breaking it and
     moving forward
    2. calling for the second half in whcih setting the data after lunch process and then stopping when all the data
     for that track ends and adding netwroking event to that
    :param first_half: first half value
    :param second_half: second half value
    :param temp_dict: dict of time wise total number of even t present
    :return:
    """
    track = []
    try:
        fill_val_f = 0
        fill_val_s = 0
        while fill_val_f < first_half:
            for k, v in temp_dict.items():
                if v > 0:
                    for i in range(v):
                        if fill_val_f + k <= first_half:
                            fill_val_f += k
                            temp_dict[k] = temp_dict[k] - 1
                            track.append(k)
                        else:
                            break
        while fill_val_s < second_half and sum(temp_dict.values()) > 0:
            for k, v in temp_dict.items():
                if v > 0:
                    for i in range(v):
                        if fill_val_s + k <= second_half:
                            fill_val_s += k
                            temp_dict[k] = temp_dict[k] - 1
                            track.append(k)
                        else:
                            break
            if fill_val_s != second_half:
                # rem = second_half - fill_val_s
                # light_val = rem / light_count
                break
    except Exception as e:
        print(e.args)
    return track


def get_index_wise_time_bassed_list(test_input):
    """
    function to get the insdex wise time based list which will be used for all the calculation1
    1. first setting the variables and then iterating to all the test input given
    2. splitting them and getting the time from that
    3. making the dict accordingly ana taking care for lighting event
    4. maintaining the count for lightning count also
    :param test_input: input in original form
    :return:
    """
    time_dict = {}
    ind = 0
    ind_dict = {}
    tot = 0
    light_count = 0
    try:
        for t in test_input:
            m = t.split()[-1].strip()
            if not 'lightning' in m:
                m = int(m[:-3])
                if not time_dict.get(m):
                    time_dict[m] = 0
                    ind_dict[m] = []
                time_dict[m] += 1
                ind_dict[m].append(ind)
                tot += m
            else:
                light_count += 1
                if not ind_dict.get('lightning'):
                    ind_dict['lightning'] = []
                ind_dict['lightning'].append(ind)
            ind += 1
    except Exception as e:
        print(e.args)
    return tot, ind_dict, time_dict, light_count
