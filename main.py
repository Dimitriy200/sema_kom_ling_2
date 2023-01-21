import bash_parser as bp
import parser_name as pn
import parser_name_xml_etree as pnxe
import different_name as dn
import parser_sentence as ps


def search_name():
    bp.bash_parser()
    pnxe.parser_name_xml_etree()

    with open('NSL.txt', 'r') as NSL:
        NSL = NSL.read()
        if NSL != '':
            # pn.parser_name()
            print()

    dn.different_name()


    ps.parser_sentence()


    with open('PS_out.txt', 'r') as PS:
        ps_text = PS.readlines()
        print(ps_text)
    return ps_text
