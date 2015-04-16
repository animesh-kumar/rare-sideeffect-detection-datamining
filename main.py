import operator

from mysqldb import MySQLDB
from stopwords import stopwords_hashset

def connect_db():
    db = MySQLDB()
    query = 'select * from temp'
    db.executequery(query)


drugs_map = {}
count_to_show = 1

def map_drugs_and_family():
    myfile = open("drugs", "r")
    for line in myfile:
        arr = line.split("=")
        drugs_family = arr[0].lower()
        drugs_list = arr[1].lower()

        drugs_name = drugs_list.split(",")
        drugs_name_list = []
        for each_drug in drugs_name:
            drugs_name_list.append(each_drug.strip())
        drugs_map[drugs_family] = drugs_name_list

    return


def print_drugs_map():
    for drugs_family in drugs_map:
        print
        print drugs_family
        for each_drugs in drugs_map.get(drugs_family):
            print each_drugs,
        print
    return


drugs_sideeffects_file = {'Author-Flagyl-SideEffects.tsv', 'Author-Ibuprofen-SideEffects.tsv',
                          'Author-Metformin-SideEffects.tsv', 'Author-Prilosec-SideEffects.tsv',
                          'Author-Tirosint-SideEffects.tsv', 'Author-Xanax-SideEffects.tsv'}

# drugs_sideeffects_file = {'Temp-Flagyl-SideEffects.tsv'}

total_drugstype_author_sideeffects_list = []       # total drugstype, author, sideeffects list
top_sideeffects_per_drugstype_map = {}             # per drugtype which are the top side effects
top_sideeffects_per_drugtype_author_list_map = {}  # per drug type per top side effects who are the authors

def extract_drugstype_author_sideeffects():
    try:
        for filename in drugs_sideeffects_file:
            drugstype = filename.split('-')[1].lower()
            myfile = open(filename, 'r')
            each_drugstype_author_sideeffects_map = dict()
            each_drugstype_author_sideeffects_map[drugstype] = {}

            for line in myfile:
                line = line.lower()
                arr = line.split('\t')
                author_id = arr[0]

                if len(arr) < 3:
                    continue

                sideeffects = arr[2][1:len(arr[2]) - 2]
                my_sideeffects_count_map = dict()

                if drugstype in each_drugstype_author_sideeffects_map and author_id in each_drugstype_author_sideeffects_map[drugstype]:
                    my_sideeffects_count_map = each_drugstype_author_sideeffects_map[drugstype][author_id]

                symptoms_arr = sideeffects.split(',')
                for each_sideeffects_and_count in symptoms_arr:
                    if len(each_sideeffects_and_count.split("=")) < 2:
                        continue
                    each_sideeffects = each_sideeffects_and_count.split("=")[0].strip()
                    symptom_count = each_sideeffects_and_count.split("=")[1].strip()
                    # print each_sideeffects, ' ', symptom_count
                    if each_sideeffects in my_sideeffects_count_map:
                        my_sideeffects_count_map[each_sideeffects] += symptom_count
                    else:
                        my_sideeffects_count_map[each_sideeffects] = symptom_count

                if len(my_sideeffects_count_map) > 0:
                    each_drugstype_author_sideeffects_map[drugstype][author_id] = my_sideeffects_count_map

            total_drugstype_author_sideeffects_list.append(each_drugstype_author_sideeffects_map)

        # print total_drugstype_author_symptoms_list;

    except Exception as ex:
        print 'Got RTE' , ' ', ex


def print_total_drugstype_author_sideeffects():
    for item in total_drugstype_author_sideeffects_list:
            for each_drugstype in item:
                for each_author_id in item[each_drugstype]:
                    print each_drugstype, ' ', each_author_id, ' ', item[each_drugstype][each_author_id]
    return


def top_sideeffects_per_drugstype():
    for each_drugstype_map in total_drugstype_author_sideeffects_list:
        for drugstype in each_drugstype_map:
            total_sideeffects_count_map = {}
            top_sideeffects_per_drugtype_author_list_map[drugstype] = {}
            for author_id in each_drugstype_map[drugstype]:
                author_sideeffects_count_map = each_drugstype_map[drugstype][author_id]

                for each_sideeffects in author_sideeffects_count_map:
                    if each_sideeffects not in total_sideeffects_count_map and each_sideeffects not in stopwords_hashset:
                        author_list = get_authour_count_for_sideeffects(drugstype, each_sideeffects, each_drugstype_map)
                        author_count_for_sideeffects = len(author_list)
                        total_sideeffects_count_map[each_sideeffects] = author_count_for_sideeffects
                        top_sideeffects_per_drugtype_author_list_map[drugstype][each_sideeffects] = author_list[0:min(count_to_show, len(author_list))]

            sorted_items = sorted(total_sideeffects_count_map.items(), key=operator.itemgetter(1))
            sorted_items.reverse()
            print sorted_items
            top_sideeffects_per_drugstype_map[drugstype] = sorted_items

    # print_top_sideeffects_per_drugstype_map()


def get_authour_count_for_sideeffects(drugstype, each_sideeffects, each_drugstype_map):
    author_list = []
    for author_id in each_drugstype_map[drugstype]:
        if each_sideeffects in each_drugstype_map[drugstype][author_id]:
            author_list.append(author_id)
    return author_list


def print_top_sideeffects_per_drugstype_map():

    for each_drugstype in top_sideeffects_per_drugstype_map:
        max_count = 0
        print each_drugstype, ' ',
        for each_sideeffects in top_sideeffects_per_drugstype_map[each_drugstype]:
            print each_sideeffects[0], ' ',
            max_count += 1
            if max_count >= count_to_show:
                break
        print
    return


def print_top_author_list_per_drugstype_per_sideeffects():
    for each_drugstype in top_sideeffects_per_drugstype_map:
        count = 0
        for each_sideeffects in top_sideeffects_per_drugstype_map[each_drugstype]:
            # if each_sideeffects in top_sideeffects_per_drugtype_author_list_map[each_drugstype]:
            print each_drugstype, ' ', each_sideeffects[0], ' = ', top_sideeffects_per_drugtype_author_list_map[each_drugstype][each_sideeffects[0]], ' '
            count += 1
            if count >= count_to_show:
                break
        print

import networkx as nx
import matplotlib.pyplot as plt


def construct_graph():
    graph = []
    for each_drugstype in top_sideeffects_per_drugstype_map:
        count1 = 0
        for each_sideeffects in top_sideeffects_per_drugstype_map[each_drugstype]:
            count2 = 0
            graph.append((each_drugstype, each_sideeffects[0]))
            for each_author in top_sideeffects_per_drugtype_author_list_map[each_drugstype][each_sideeffects[0]]:
                graph.append((each_sideeffects[0], each_author))
                count2 += 1
                if count2 >= count_to_show:
                    break
            count1 += 1
            if count1 >= count_to_show:
                break;
    return graph


def draw_graph(labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    graph = construct_graph()

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness, alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size, font_family=text_font)

    if labels is None:
        labels = range(len(graph))



    # edge_labels = dict(zip(graph, labels))
    # nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, label_pos=edge_text_pos)

    # show graph
    plt.show()


if __name__ == '__main__':
    # connect_db()

    map_drugs_and_family()
    # print_drugs_map()

    extract_drugstype_author_sideeffects()
    # print_total_drugstype_author_sideeffects()


    top_sideeffects_per_drugstype()
    print_top_sideeffects_per_drugstype_map()
    print
    print_top_author_list_per_drugstype_per_sideeffects()

    draw_graph()

