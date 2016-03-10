# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 TrustCode - www.trustcode.com.br                         #
#              Danimar Ribeiro <danimaribeiro@gmail.com>                      #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################

import re
import string
from datetime import datetime

from openerp import pooler
from openerp.osv import orm
from openerp.tools.translate import _
from openerp.addons.l10n_br_account_product.sped.nfe.document import NFe310

class NFCe310(NFe310):

    def __init__(self):
        super(NFCe310, self).__init__()
        self.total_icms = 0.00

    def _total(self, cr, uid, ids, inv, context=None):

        #
        # Totais
        #
        self.nfe.infNFe.total.ICMSTot.vBC.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vICMS.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vBCST.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vST.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vProd.valor = str("%.2f" % inv.amount_total)
        self.nfe.infNFe.total.ICMSTot.vFrete.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vSeg.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vDesc.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vII.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vIPI.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vPIS.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vCOFINS.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vOutro.valor = str("%.2f" % 0.00)
        self.nfe.infNFe.total.ICMSTot.vNF.valor = str("%.2f" % inv.amount_total)

    def _details(self, cr, uid, ids, inv, inv_line, i, context=None):

        #
        # Detalhe
        #

        self.det.nItem.valor = i
        self.det.prod.cProd.valor = inv_line.product_id.code or ''
        self.det.prod.cEAN.valor = inv_line.product_id.ean13 or ''
        self.det.prod.xProd.valor = inv_line.product_id.name or ''
        self.det.prod.NCM.valor = re.sub('[%s]' % re.escape(
            string.punctuation), '', inv_line.product_id.ncm_id.name or '')
        self.det.prod.EXTIPI.valor = ''
        self.det.prod.CFOP.valor = '5102'
        self.det.prod.uCom.valor = inv_line.product_id.uom_id.name or ''
        self.det.prod.qCom.valor = str("%.4f" % inv_line.qty)
        self.det.prod.vUnCom.valor = str("%.7f" % (inv_line.price_unit))
        self.det.prod.vProd.valor = str("%.2f" % inv_line.price_subtotal_incl)
        self.det.prod.cEANTrib.valor = inv_line.product_id.ean13 or ''
        self.det.prod.uTrib.valor = self.det.prod.uCom.valor
        self.det.prod.qTrib.valor = self.det.prod.qCom.valor
        self.det.prod.vUnTrib.valor = self.det.prod.vUnCom.valor        
        #
        # Produto entra no total da NF-e
        #
        self.det.prod.indTot.valor = 1

        # if inv_line.icms_cst_id.code > 100:
        #     self.det.imposto.ICMS.CSOSN.valor = inv_line.icms_cst_id.code
        #     self.det.imposto.ICMS.pCredSN.valor = str("%.2f" % inv_line.icms_percent)
        #     self.det.imposto.ICMS.vCredICMSSN.valor = str("%.2f" % inv_line.icms_value)

        self.det.imposto.ICMS.CST.valor = '41'
        #self.det.imposto.ICMS.modBC.valor = '3'
        #self.det.imposto.ICMS.vBC.valor = str("%.2f" %
        # inv_line.price_subtotal_incl)
        # self.det.imposto.ICMS.pRedBC.valor = str("%.2f" % inv_line.icms_percent_reduction)
        #self.det.imposto.ICMS.pICMS.valor = str("%.2f" % icms)
        #self.det.imposto.ICMS.vICMS.valor = str("%.2f" % icms_value)

        #self.total_icms += icms_value

        # # IPI        
        self.det.imposto.IPI.cEnq.valor = ''        

        # # PIS
        self.det.imposto.PIS.CST.valor = '99'        
        
        # # COFINS
        self.det.imposto.COFINS.CST.valor = '99'        
        

    def _receiver(self, cr, uid, ids, inv, company, nfe_environment, context=None):
        if not inv.partner_id:
            return
        #
        # Destinatário
        #
        partner_bc_code = ''
        address_invoice_state_code = ''
        address_invoice_city = ''
        partner_cep = ''

        if inv.partner_id.country_id.bc_code:
            partner_bc_code = inv.partner_id.country_id.bc_code[1:]

        if inv.partner_id.country_id.id != company.country_id.id:
            address_invoice_state_code = 'EX'
            address_invoice_city = 'Exterior'
            partner_cep = ''
        else:
            address_invoice_state_code = inv.partner_id.state_id.code
            address_invoice_city = inv.partner_id.l10n_br_city_id.name or ''
            partner_cep = re.sub('[%s]' % re.escape(string.punctuation), '', str(inv.partner_id.zip or '').replace(' ',''))

        # Se o ambiente for de teste deve ser
        # escrito na razão do destinatário
        if nfe_environment == '2':
            self.nfe.infNFe.dest.xNome.valor = 'NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL'
        else:
            self.nfe.infNFe.dest.xNome.valor = inv.partner_id.legal_name or ''

        if inv.partner_id.is_company:
            self.nfe.infNFe.dest.CNPJ.valor = re.sub('[%s]' % re.escape(string.punctuation), '', inv.partner_id.cnpj_cpf or '')
            self.nfe.infNFe.dest.IE.valor = re.sub('[%s]' % re.escape(string.punctuation), '', inv.partner_id.inscr_est or '')
        else:
            self.nfe.infNFe.dest.CPF.valor = re.sub('[%s]' % re.escape(string.punctuation), '', inv.partner_id.cnpj_cpf or '')

        self.nfe.infNFe.dest.enderDest.xLgr.valor = inv.partner_id.street or ''
        self.nfe.infNFe.dest.enderDest.nro.valor = inv.partner_id.number or ''
        self.nfe.infNFe.dest.enderDest.xCpl.valor = inv.partner_id.street2 or ''
        self.nfe.infNFe.dest.enderDest.xBairro.valor = inv.partner_id.district or 'Sem Bairro'
        self.nfe.infNFe.dest.enderDest.cMun.valor = '%s%s' % (inv.partner_id.state_id.ibge_code, inv.partner_id.l10n_br_city_id.ibge_code)
        self.nfe.infNFe.dest.enderDest.xMun.valor = address_invoice_city
        self.nfe.infNFe.dest.enderDest.UF.valor = address_invoice_state_code
        self.nfe.infNFe.dest.enderDest.CEP.valor = partner_cep
        self.nfe.infNFe.dest.enderDest.cPais.valor = partner_bc_code
        self.nfe.infNFe.dest.enderDest.xPais.valor = inv.partner_id.country_id.name or ''
        self.nfe.infNFe.dest.enderDest.fone.valor = re.sub('[%s]' % re.escape(string.punctuation), '', str(inv.partner_id.phone or '').replace(' ',''))
        self.nfe.infNFe.dest.email.valor = inv.partner_id.email or ''


    def _nfe_identification(self, cr, uid, ids, inv, company, nfe_environment, context=None):

        # Identificação da NF-e
        #
        self.nfe.infNFe.ide.cUF.valor = company.state_id and company.state_id.ibge_code or ''
        self.nfe.infNFe.ide.cNF.valor = ''
        self.nfe.infNFe.ide.indPag.valor = '0'
        self.nfe.infNFe.ide.serie.valor = 20
        self.nfe.infNFe.ide.nNF.valor = inv.id or ''
        self.nfe.infNFe.ide.cMunFG.valor = ('%s%s') % (company.state_id.ibge_code, company.l10n_br_city_id.ibge_code)
        self.nfe.infNFe.ide.dhEmi.valor = datetime.strptime(inv.date_order,
                                                            '%Y-%m-%d %H:%M:%S')
#        self.nfe.infNFe.ide.dhSaiEnt.valor = datetime.strptime(
# inv.date_order, '%Y-%m-%d %H:%M:%S')

    def _nfe_operation(self, cr, uid, ids, inv, company, nfe_environment,
                       context=None):
        # Dados da operação
        self.nfe.infNFe.ide.natOp.valor = 'Venda'
        self.nfe.infNFe.ide.mod.valor = '65'
        self.nfe.infNFe.ide.tpImp.valor = '4'  # (1 - Retrato; 2 - Paisagem)
        self.nfe.infNFe.ide.indPres.valor = '1'
        self.nfe.infNFe.ide.indFinal.valor = '1'
        self.nfe.infNFe.ide.tpNF.valor = '1'
        self.nfe.infNFe.ide.idDest.valor = '1'
        self.nfe.infNFe.ide.verProc.valor = 'Odoo v8'
        self.nfe.infNFe.ide.tpAmb.valor = nfe_environment
        self.nfe.infNFe.ide.finNFe.valor = 1
        self.nfe.infNFe.ide.procEmi.valor = 0
        self.nfe.infNFe.ide.tpEmis.valor = 1

    def get_NFe(self):

        try:
            from pysped.nfe.leiaute import NFCe_310
        except ImportError:
            raise orm.except_orm(_(u'Erro!'), _(u"Biblioteca PySPED não instalada!"))

        return NFCe_310()

    def _get_NFRef(self):

        try:
            from pysped.nfe.leiaute import NFCe_310
        except ImportError:
            raise orm.except_orm(_(u'Erro!'), _(u"Biblioteca PySPED não instalada!"))

        return NFCe_310()

    def _serializer(self, cr, uid, ids, nfe_environment, context=None):

        pool = pooler.get_pool(cr.dbname)
        nfes = []

        if not context:
            context = {'lang': 'pt_BR'}

        for order in pool.get('pos.order').browse(cr, uid, ids, context):

            company = pool.get('res.partner').browse(
                cr, uid, order.company_id.partner_id.id, context)

            self.nfe = self.get_NFe()
            
            self._nfe_operation(
                cr, uid, ids, order, company, nfe_environment, context)

            self._nfe_identification(
                cr, uid, ids, order, company, nfe_environment, context)

            self._emmiter(cr, uid, ids, order, company, context)
            self._receiver(cr, uid, ids, order, company, nfe_environment, context)

            i = 0
            for lines in order.lines:
                i += 1
                self.det = self._get_Det()
                self._details(cr, uid, ids, order, lines, i, context)
                self.nfe.infNFe.det.append(self.det)

            if order.sale_journal.revenue_expense:
                pass
                # for line in inv.move_line_receivable_id:
                #     self.dup = self._get_Dup()
                #     self._encashment_data(cr, uid, ids, inv, line, context)
                #     self.nfe.infNFe.cobr.dup.append(self.dup)

            # self._additional_information(cr, uid, ids, inv, context)
            self._total(cr, uid, ids, order, context)

            # Gera Chave da NFe
            self.nfe.gera_nova_chave()
            url = self.nfe.monta_url_qrcode('00001')
            self.nfe.infNFeSupl.qrCode.valor = url
            nfes.append(self.nfe)

        return nfes

    def get_nfce(self, cr, uid, ids, nfe_environment, context=None):
        """"""
        return self._serializer(cr, uid, ids, nfe_environment, context)
