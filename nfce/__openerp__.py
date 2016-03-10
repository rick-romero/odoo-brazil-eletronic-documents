# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Luis Felipe Mileo - KMEE                                 #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU General Public License for more details.                                 #
#                                                                             #
#You should have received a copy of the GNU General Public License            #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################

{
    'name': 'NFC-e Cupom Eletrônico Brasileiro',
    'version': '8.0.0.0.1',
    'category': 'Point of Sale',
    'description': """Implementacão da notas fiscais do consumidor
    eletrônica / NFC-E """,
    'author': 'KMEE, Trustcode',
    'license': 'AGPL-3',
    'website': 'http://github.com/odoo-brazil',
    'description': """
    """,
    'depends': [
        'nfe',
        'point_of_sale',
    ],
    'data': [ 
        'views/pos_order_view.xml',
        'views/point_of_sale.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
}
