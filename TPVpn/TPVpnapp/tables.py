#    -*- coding: UTF-8 -*-
#
#    --- License block --------------------------------------------------------
#    This file is part of TPVpn.
#
#    TPVpn is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TPVpn is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TPVpn.  If not, see <http://www.gnu.org/licenses/>.
#    --- End of License block -------------------------------------------------


import django_tables2 as tables


class ProductTable(tables.Table):
    image = tables.TemplateColumn(verbose_name='Imagen', orderable=False,
                                  template_name='tables/image_column.html')
    barCode = tables.Column(verbose_name='Código de Barras')
    name = tables.TemplateColumn(verbose_name='Nombre del Producto',
                                 template_name='tables/name_column.html')
    provider = tables.TemplateColumn(
        verbose_name='Proveedor (Marca)',
        template_name='tables/provider_column.html')
    category = tables.Column(verbose_name='Categoría')
    bsprice = tables.TemplateColumn(verbose_name='Compra / Venta',
                                    template_name='tables/price_column.html',
                                    orderable=False)
    offer = tables.Column(accessor='offer.offer', verbose_name='Oferta (€)')
    stock = tables.TemplateColumn(verbose_name='Existencias',
                                  template_name='tables/stock_column.html',
                                  orderable=False)
    options = tables.TemplateColumn(verbose_name='Opciones', orderable=False,
                                    template_name='tables/options_column.html')

    class Meta:
        attrs = {'class': 'table table-striped projects'}


class CategoryTable(tables.Table):
    name = tables.Column(verbose_name='Nombre')
    edit = tables.TemplateColumn(verbose_name='Editar',
                                 template_name='tables/edit_column.html')

    class Meta:
        attrs = {'class': 'table table-striped projects'}
