#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
