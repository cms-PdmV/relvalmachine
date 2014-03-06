/**
 * Created by Zygimantas Gatelis on 3/5/14.
 */
"use strict";

describe('Alerts Service', function() {

    var alertsService;

    beforeEach(module('relvalServices'));

    beforeEach(function() {
        var $injector = angular.injector([ 'relvalServices' ]);
        alertsService = $injector.get( 'AlertsService' );
    });

    afterEach(function() {
        alertsService.setTimeout(5000)
    })



    it('should have none alerts at first', function() {
        var alerts = alertsService.fetchAlerts();
        expect(alerts.length).toBe(0);
    });

    it('should remove alert automatically after timeout', function() {
        alertsService.setTimeout(500);
        alertsService.addError("Error");
        waitsFor(function() {
            return alertsService.fetchAlerts().length == 0
        }, "Alert wasn't removed", 600);
    });

    it('should add all kind of alerts', function() {
        alertsService.addError({msg: "danger"});
        alertsService.addSuccess({msg: "success"});
        alertsService.addWarn({msg: "warning"});

        var alerts = alertsService.fetchAlerts();
        var types = ['danger', 'success', 'warning'];
        for(var i=0; i < 3; i++) {
            expect(alerts[i].type).toBe(types[i]);
            expect(alerts[i].msg).toBe(types[i]);
        }
    });

    it('should remove alert when remove presed', function() {
        alertsService.addError("Error");
        alertsService.close(0);
        expect(alertsService.fetchAlerts().length).toBe(0);
    });
});
