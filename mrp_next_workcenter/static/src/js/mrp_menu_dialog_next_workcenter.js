/** @odoo-module **/

import { MrpMenuDialog } from '@mrp_workorder/mrp_display/dialog/mrp_menu_dialog';
import { patch } from '@web/core/utils/patch';
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { MrpWorkcenterDialog } from "@mrp_workorder/mrp_display/dialog/mrp_workcenter_dialog";

patch(MrpMenuDialog.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.dialogService = useService("dialog");
        this.notification = useService("notification");
    },

    async nextWorkcenter() {
        // Función que se ejecutará cuando el usuario seleccione un workcenter
        function _processNextWorkcenter(workcenters) {
            if (!workcenters.length) return;

            const workcenter = workcenters[0];
            // Llamar al método process_next_workcenter
            this.orm.call(
                "mrp.workorder",
                "process_next_workcenter",
                [[this.props.record.resId], workcenter.id]
            ).then(() => {
                this.notification.add(_t("Workcenter processed successfully"), {
                    type: "success",
                });
                this.props.close();
            }).catch((error) => {
                console.error("Error en process_next_workcenter:", error);
                this.notification.add(_t("Error al procesar el workcenter"), {
                    type: "danger",
                });
            });
        }

        try {
            // Obtener los workcenters disponibles llamando al método Python
            const nextWorkcenters = await this.orm.call(
                "mrp.workorder",
                "get_next_worcenter_ids",
                [[this.props.record.resId]]
            );

            if (!nextWorkcenters || !nextWorkcenters.length) {
                this.notification.add(_t("No next workcenters configured for this order."), {
                    type: "warning",
                });
                return;
            }

            // Formatear los workcenters para el diálogo
            const formattedWorkcenters = nextWorkcenters.map(wc => ({
                id: wc[0],
                display_name: wc[1]
            }));

            // Configurar los parámetros del diálogo
            const params = {
                title: _t("Select next work center"),
                confirm: _processNextWorkcenter.bind(this),
                radioMode: true,
                workcenters: formattedWorkcenters,
            };

            // Mostrar el diálogo
            this.dialogService.add(MrpWorkcenterDialog, params);
        } catch (error) {
            console.error("Error getting the next workcenters:", error);
            this.notification.add(_t("Failed to retrieve the next workcenters"), {
                type: "danger",
            });
        }
    },
});