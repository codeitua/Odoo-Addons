from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import datetime
from odoo.addons.mail.tests.common import mail_new_test_user

class TestContractHandover(TransactionCase):

    def get_available_contracts(self,user_val):
        return user_val.with_user(user_val.id).get_contract_ids()

    def new_contract_handover_rule(self,department,provider,receiver,date_end,share_manager=False):
        return self.env['contract.handover.rule'].sudo().create({
            'department_id': department,
            'access_provider_id': provider,
            'access_receiver_id': receiver,
            'expiration_date': date_end,
            'share_to_manager': share_manager,
        })

    def new_contract(self, state, empl, kanban_state, start, end=None):
        return self.env['hr.contract'].sudo().create({
            'name': 'Contract',
            'employee_id': empl,
            'state': state,
            'kanban_state': kanban_state,
            'wage': 1,
            'date_start': start,
            'date_end': end,
        })

    def setUp(self, *args, **kwargs):
        super(TestContractHandover, self).setUp(*args, **kwargs)

        self.handover_manager1 = mail_new_test_user(self.env, login='hm1', groups='hr_contract.group_hr_contract_manager', name='Handover manager1', email='hm1@example.com')
        self.handover_manager2 = mail_new_test_user(self.env, login='hm2', groups='hr_contract.group_hr_contract_manager', name='Handover manager2', email='hm2@example.com')
        self.handover_receiver1 = mail_new_test_user(self.env, login='hr1', groups='base.group_user', name='Handover receiver1', email='hr2@example.com')
        self.handover_receiver2 = mail_new_test_user(self.env, login='hr2', groups='base.group_user', name='Handover receiver2', email='hr3@example.com')
        
        self.hand_user1 = mail_new_test_user(self.env, login='he1', groups='base.group_user,hr.group_hr_user', name='Handover user1', email='he1@example.com')
        self.hand_user2 = mail_new_test_user(self.env, login='he2', groups='base.group_user,hr.group_hr_user', name='Handover user2', email='he2@example.com')
        self.hand_user3 = mail_new_test_user(self.env, login='he3', groups='base.group_user,hr.group_hr_user', name='Handover user3', email='he3@example.com')
        self.hand_user4 = mail_new_test_user(self.env, login='he4', groups='base.group_user,hr.group_hr_user', name='Handover user4', email='he4@example.com')
        self.hand_user5 = mail_new_test_user(self.env, login='he5', groups='base.group_user,hr.group_hr_user', name='Handover user5', email='he5@example.com')
        self.hand_user6 = mail_new_test_user(self.env, login='he6', groups='base.group_user,hr.group_hr_user', name='Handover user6', email='he6@example.com')

        self.department1 = self.env['hr.department'].create({
            'name': 'Test Department1',
        })

        self.department2 = self.env['hr.department'].create({
            'name': 'Test Department2',
        })

        self.department3 = self.env['hr.department'].create({
            'name': 'Test Department2',
        })

        self.empl1 = self.env['hr.employee'].create({'user_id': self.hand_user1.id,
                                                    'department_id':self.department1.id})
        self.department1.manager_id = self.empl1.id
        
        self.empl2 = self.env['hr.employee'].create({'user_id': self.hand_user2.id,
                                                'department_id':self.department1.id})
        self.empl3 = self.env['hr.employee'].create({'user_id': self.hand_user3.id,
                                                'department_id':self.department1.id})
        self.empl4 = self.env['hr.employee'].create({'user_id': self.hand_user4.id,
                                                'department_id':self.department2.id})
        self.empl5 = self.env['hr.employee'].create({'user_id': self.hand_user5.id,
                                                'department_id':self.department3.id})

        self.contract_start = datetime.date.today() - datetime.timedelta(days=5)
        self.contract_end = datetime.date.today() + datetime.timedelta(days=15)

        self.contract1 = self.new_contract('draft',self.empl1.id, 'normal', self.contract_start, self.contract_end)
        self.contract1._compute_employee_contract()
        self.contract2 = self.new_contract('draft',self.empl2.id, 'normal', self.contract_start, self.contract_end)
        self.contract2._compute_employee_contract()

        self.contract3 = self.new_contract('draft',self.empl3.id, 'normal', self.contract_start, self.contract_end)
        self.contract3._compute_employee_contract()
        self.contract4 = self.new_contract('draft',self.empl4.id, 'normal', self.contract_start, self.contract_end)
        self.contract4._compute_employee_contract()
        self.contract5 = self.new_contract('open',self.empl5.id, 'normal', self.contract_start, self.contract_end)
        self.contract5._compute_employee_contract()

    
    # raises error when try to run without commenting  _validate_expiration_date()
    # becuase we nee to generate rule with old date and get validation error
    # def test_cron_job(self):
    #     """Check Crone-----------------------------"""
    #     self.last_rule = self.new_contract_handover_rule(
    #         self.department1.id,
    #         self.handover_manager1.id,
    #         self.hand_user1.id,
    #         datetime.date.today() - datetime.timedelta(days=4)
    #     )
    #     self.assertEqual(len(self.env['contract.handover.rule'].search([])), 1, 'rule count needs to be 1')
    #     self.env['contract.handover.rule'].delete_expired_rules()
    #     self.assertEqual(len(self.env['contract.handover.rule'].search([])), 0, 'rule count needs to be 0')



    def test_date_validation(self):
        with self.assertRaises(ValidationError, msg="Please select a later date."):
            self.new_contract_handover_rule(
                self.department1.id,
                self.handover_manager1.id,
                self.handover_receiver1.id,
                datetime.date.today() - datetime.timedelta(days=4)
            )
    

    def test_check_rule_visibility(self):
        # Check manager can see all contracts
        m_c1 = self.get_available_contracts(self.handover_manager1)
        self.assertGreater(len(m_c1), 0, 'contract count needs to be greater 0')

        # Check not shared users can't see any contracts
        u_c1 = self.get_available_contracts(self.handover_receiver1)
        self.assertEqual(len(u_c1), 0, 'contract count needs to be 0')

        u_c2 = self.get_available_contracts(self.handover_receiver2)
        self.assertEqual(len(u_c2), 0, 'contract count needs to be 0')

        # create rule for receiver and check available contracts amount
        self.contr_handover_rule1 = self.env['contract.handover.rule'].sudo().create({
            'department_id': self.department1.id,
            'access_provider_id': self.handover_manager1.id,
            'access_receiver_id': self.handover_receiver1.id,
            'expiration_date': None,
            'share_to_manager': False,
        })
        av_contracts = self.get_available_contracts(self.handover_receiver1)

        # Check that after sharing receiver1 can see contracts
        self.assertGreater(len(av_contracts), 0, 'contract count needs to be greater than 0')

        # Check that receiver1 cant see department managers contracts
        # Because rule have share_to_manager field = False
        self.assertNotIn(self.contract1.id,av_contracts,'Contract 1 dont need to be in result')

        # create rule for receiver and check available contracts amount
        self.contr_handover_rule2 = self.env['contract.handover.rule'].sudo().create({
            'department_id': self.department1.id,
            'access_provider_id': self.handover_manager2.id,
            'access_receiver_id': self.handover_receiver2.id,
            'expiration_date': datetime.date.today() + datetime.timedelta(days=4),
            'share_to_manager': True,
        })
        av_contracts2 = self.get_available_contracts(self.handover_receiver2)

        # Check that after sharing receiver1 can see contracts
        self.assertGreater(len(av_contracts2), 0, 'contract count needs to be greater than 0')

        # Check that receiver1 can see department managers contracts
        # Because rule have share_to_manager field = True
        self.assertIn(self.contract1.id,av_contracts2,'Contract 1 need to be in result')


        #check rule deletion when department deleted
        rule_qty = len(self.env['contract.handover.rule'].search([]))
        self.department1.unlink()
        self.assertGreater(rule_qty,len(self.env['contract.handover.rule'].search([])),'Qty of rules needs to be changed')
        
        m_c1 = self.get_available_contracts(self.handover_manager1)
        self.assertGreater(len(m_c1), 0, 'contract count needs to be greater 0')

        # Check not shared users can't see any contracts
        u_c1 = self.get_available_contracts(self.handover_receiver1)
        self.assertEqual(len(u_c1), 0, 'contract count needs to be 0')

        u_c2 = self.get_available_contracts(self.handover_receiver2)
        self.assertEqual(len(u_c2), 0, 'contract count needs to be 0')